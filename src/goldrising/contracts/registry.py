"""指标注册表：indicators/registry.yaml 的加载与校验。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

VALID_TIERS: frozenset[str] = frozenset({"1", "2", "3", "target"})
VALID_FREQUENCIES: frozenset[str] = frozenset({"daily", "weekly", "monthly", "quarterly"})
VALID_UNITS: frozenset[str] = frozenset(
    {"pct", "pctl", "usd", "index", "ratio", "contracts", "tonnes", "bp", "pct_change", "count"}
)
KNOWN_PROVIDERS: frozenset[str] = frozenset(
    {
        "treasury",
        "nyfed",
        "cboe",
        "fred",
        "yahoo",
        "yahoo_gc_contract",
        "cftc",
        "spdr",
        "fedfunds",
        "manual",
        "tushare",
        "derived",
    }
)
DERIVED_OPS: frozenset[str] = frozenset(
    {"sub", "div", "mul", "pct_rank", "ma_dist", "mom", "beta", "lev_decay", "ratio_pct_change_diff"}
)


class RegistryError(ValueError):
    pass


@dataclass(frozen=True)
class Source:
    provider: str
    series: str = ""
    symbol: str = ""
    publisher: str = ""
    url: str = ""
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Derived:
    op: str
    inputs: tuple[str, ...]
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Indicator:
    id: str
    name: str
    group: str
    tier: str
    unit: str
    decimals: int
    frequency: str
    lag_days: int
    gold_sign: int
    source: Source
    collect: bool = True
    derived: Derived | None = None
    narratives: tuple[str, ...] = ()
    note: str = ""
    stage: int = 1

    @property
    def is_derived(self) -> bool:
        return self.derived is not None


@dataclass(frozen=True)
class GroupMeta:
    id: str
    name: str
    order: int
    question: str = ""


@dataclass(frozen=True)
class Registry:
    version: int
    groups: tuple[GroupMeta, ...]
    indicators: tuple[Indicator, ...]

    def by_id(self, indicator_id: str) -> Indicator:
        for ind in self.indicators:
            if ind.id == indicator_id:
                return ind
        raise KeyError(indicator_id)

    def has(self, indicator_id: str) -> bool:
        return any(ind.id == indicator_id for ind in self.indicators)

    def group(self, group_id: str) -> GroupMeta:
        for g in self.groups:
            if g.id == group_id:
                return g
        raise KeyError(group_id)

    def collectable(self) -> list[Indicator]:
        return [i for i in self.indicators if i.collect and not i.is_derived]

    def derived_in_order(self) -> list[Indicator]:
        """派生指标按依赖拓扑排序。"""
        pending = {i.id: i for i in self.indicators if i.is_derived and i.collect}
        done: set[str] = {i.id for i in self.indicators if not i.is_derived}
        ordered: list[Indicator] = []
        while pending:
            progressed = False
            for iid, ind in list(pending.items()):
                assert ind.derived is not None
                if all(dep in done for dep in ind.derived.inputs):
                    ordered.append(ind)
                    done.add(iid)
                    del pending[iid]
                    progressed = True
            if not progressed:
                raise RegistryError(f"派生指标存在循环依赖或缺失输入: {sorted(pending)}")
        return ordered

    def validate(self) -> None:
        ids = [i.id for i in self.indicators]
        dupes = sorted({x for x in ids if ids.count(x) > 1})
        if dupes:
            raise RegistryError(f"重复的指标 id: {dupes}")
        group_ids = {g.id for g in self.groups}
        for ind in self.indicators:
            if ind.group not in group_ids:
                raise RegistryError(f"{ind.id}: 未知因子组 {ind.group}")
            if ind.tier not in VALID_TIERS:
                raise RegistryError(f"{ind.id}: 非法级别 {ind.tier}")
            if ind.frequency not in VALID_FREQUENCIES:
                raise RegistryError(f"{ind.id}: 非法频率 {ind.frequency}")
            if ind.unit not in VALID_UNITS:
                raise RegistryError(f"{ind.id}: 非法单位 {ind.unit}")
            if ind.source.provider not in KNOWN_PROVIDERS:
                raise RegistryError(f"{ind.id}: 未知数据提供方 {ind.source.provider}")
            if ind.gold_sign not in (-1, 0, 1):
                raise RegistryError(f"{ind.id}: gold_sign 必须是 -1、0、1")
            if ind.derived is not None:
                if ind.source.provider != "derived":
                    raise RegistryError(f"{ind.id}: 派生指标的 provider 必须为 derived")
                if ind.derived.op not in DERIVED_OPS:
                    raise RegistryError(f"{ind.id}: 未知派生运算 {ind.derived.op}")
                for dep in ind.derived.inputs:
                    if dep not in ids:
                        raise RegistryError(f"{ind.id}: 派生输入 {dep} 不存在")
            elif ind.source.provider == "derived":
                raise RegistryError(f"{ind.id}: provider 为 derived 但缺少 derived 定义")
        self.derived_in_order()


def _parse_indicator(raw: dict[str, Any]) -> Indicator:
    src_raw = dict(raw.get("source") or {})
    derived_raw = raw.get("derived")
    derived = None
    if derived_raw:
        derived = Derived(
            op=str(derived_raw["op"]),
            inputs=tuple(str(x) for x in derived_raw.get("inputs", [])),
            params=dict(derived_raw.get("params") or {}),
        )
    known = {"provider", "series", "symbol", "publisher", "url"}
    source = Source(
        provider=str(src_raw.get("provider", "")),
        series=str(src_raw.get("series", "")),
        symbol=str(src_raw.get("symbol", "")),
        publisher=str(src_raw.get("publisher", "")),
        url=str(src_raw.get("url", "")),
        params={k: v for k, v in src_raw.items() if k not in known},
    )
    try:
        return Indicator(
            id=str(raw["id"]),
            name=str(raw["name"]),
            group=str(raw["group"]),
            tier=str(raw["tier"]),
            unit=str(raw["unit"]),
            decimals=int(raw.get("decimals", 2)),
            frequency=str(raw["frequency"]),
            lag_days=int(raw.get("lag_days", 0)),
            gold_sign=int(raw.get("gold_sign", 0)),
            source=source,
            collect=bool(raw.get("collect", True)),
            derived=derived,
            narratives=tuple(str(x) for x in raw.get("narratives", []) or []),
            note=str(raw.get("note", "")),
            stage=int(raw.get("stage", 1)),
        )
    except KeyError as e:
        raise RegistryError(f"指标缺少必填字段 {e}: {raw.get('id', '<无 id>')}") from e


def load_registry(path: Path) -> Registry:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise RegistryError("registry.yaml 顶层必须是映射")
    groups = tuple(
        GroupMeta(
            id=str(g["id"]), name=str(g["name"]), order=int(g.get("order", 0)), question=str(g.get("question", ""))
        )
        for g in data.get("groups", [])
    )
    indicators = tuple(_parse_indicator(r) for r in data.get("indicators", []))
    reg = Registry(version=int(data.get("version", 1)), groups=groups, indicators=indicators)
    reg.validate()
    return reg
