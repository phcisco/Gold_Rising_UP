from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from goldrising.contracts import Registry

LIFECYCLE_STATES = ("新兴", "边际", "主导", "共识", "退潮", "已证伪", "归档")
PRICING_DEGREES = ("未定价", "部分", "充分", "已出清")
DIRECTIONS = ("bull", "bear", "mixed")
HORIZONS = ("weeks", "3-12m", "years")
SIGNS = ("up", "down", "flat")
WEIGHTS = ("high", "medium", "low")
COND_TYPES = ("quant", "qual")
SOURCE_TYPES = ("primary", "secondary")
STATUSES = ("active", "archived")
RULE_OPS = (
    "lt",
    "lte",
    "gt",
    "gte",
    "eq",
    "change_gt",
    "change_lt",
    "pct_change_gt",
    "pct_change_lt",
    "cross_above",
    "cross_below",
    "pctl_gt",
    "pctl_lt",
)
REQUIRED = (
    "id",
    "name",
    "status",
    "lifecycle_state",
    "lifecycle_since",
    "lifecycle_rationale",
    "pricing_degree",
    "pricing_rationale",
    "direction",
    "horizon",
    "thesis",
    "logic_chain",
    "regime_dependency",
    "evidence_indicators",
    "verification_signals",
    "falsification_conditions",
    "news_queries",
    "counterargument",
    "sources",
)


@dataclass(frozen=True)
class CardProblem:
    card_id: str
    level: str  # error | warning
    message: str

    def __str__(self) -> str:
        return f"[{self.level}] {self.card_id}: {self.message}"


def load_cards(directory: Path) -> dict[Path, dict[str, Any]]:
    """递归读取目录下全部 .yaml 叙事卡；解析失败的文件以 {'__error__': msg} 表示。"""
    cards: dict[Path, dict[str, Any]] = {}
    for path in sorted(directory.rglob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            cards[path] = data if isinstance(data, dict) else {"__error__": "顶层不是映射"}
        except yaml.YAMLError as e:
            cards[path] = {"__error__": f"YAML 解析失败: {e}"}
    return cards


def _is_date(v: object) -> bool:
    if isinstance(v, date):
        return True
    if isinstance(v, str):
        try:
            date.fromisoformat(v)
            return True
        except ValueError:
            return False
    return False


def _known_indicator(iid: str, registry: Registry | None, proposed: set[str]) -> bool:
    if iid in proposed:
        return True
    return registry is None or registry.has(iid)


def _validate_rule(
    rule: object, cid: str, where: str, registry: Registry | None, proposed: set[str]
) -> list[CardProblem]:
    problems: list[CardProblem] = []
    if not isinstance(rule, dict):
        return [CardProblem(cid, "error", f"{where}: rule 必须是映射")]
    if "all_of" in rule or "any_of" in rule:
        key = "all_of" if "all_of" in rule else "any_of"
        subs = rule.get(key)
        if not isinstance(subs, list) or not subs:
            return [CardProblem(cid, "error", f"{where}: {key} 必须是非空列表")]
        for i, sub in enumerate(subs):
            problems += _validate_rule(sub, cid, f"{where}.{key}[{i}]", registry, proposed)
        return problems
    iid = rule.get("indicator_id")
    if not isinstance(iid, str) or not iid:
        problems.append(CardProblem(cid, "error", f"{where}: rule 缺少 indicator_id"))
    elif not _known_indicator(iid, registry, proposed):
        problems.append(CardProblem(cid, "error", f"{where}: 指标 {iid} 不在注册表也不在 proposed_indicators"))
    op = rule.get("op")
    if op not in RULE_OPS:
        problems.append(CardProblem(cid, "error", f"{where}: 未知 op {op!r}"))
    if "value" not in rule or not isinstance(rule.get("value"), int | float):
        problems.append(CardProblem(cid, "error", f"{where}: value 必须是数字"))
    return problems


def validate_card(
    card: dict[str, Any], registry: Registry | None = None, path: Path | None = None
) -> list[CardProblem]:
    cid = str(card.get("id") or (path.stem if path else "<无 id>"))
    p: list[CardProblem] = []
    if "__error__" in card:
        return [CardProblem(cid, "error", str(card["__error__"]))]
    for key in REQUIRED:
        if key not in card or card[key] in (None, "", [], {}):
            p.append(CardProblem(cid, "error", f"缺少必填字段 {key}"))
    if path is not None and card.get("id") and path.stem != card["id"]:
        p.append(CardProblem(cid, "error", f"文件名 {path.name} 与 id {card['id']} 不一致"))
    if card.get("status") not in STATUSES:
        p.append(CardProblem(cid, "error", f"status 非法: {card.get('status')!r}"))
    if card.get("lifecycle_state") not in LIFECYCLE_STATES:
        p.append(CardProblem(cid, "error", f"lifecycle_state 非法: {card.get('lifecycle_state')!r}"))
    if card.get("pricing_degree") not in PRICING_DEGREES:
        p.append(CardProblem(cid, "error", f"pricing_degree 非法: {card.get('pricing_degree')!r}"))
    if card.get("direction") not in DIRECTIONS:
        p.append(CardProblem(cid, "error", f"direction 非法: {card.get('direction')!r}"))
    if card.get("horizon") not in HORIZONS:
        p.append(CardProblem(cid, "warning", f"horizon 非规范值: {card.get('horizon')!r}"))
    if "lifecycle_since" in card and not _is_date(card["lifecycle_since"]):
        p.append(CardProblem(cid, "error", "lifecycle_since 不是 ISO 日期"))
    if card.get("status") == "archived" and card.get("lifecycle_state") not in ("已证伪", "归档"):
        p.append(CardProblem(cid, "warning", "已归档的卡片 lifecycle_state 应为 已证伪 或 归档"))

    rd = card.get("regime_dependency")
    if isinstance(rd, dict):
        for k in ("passive_fed", "credible_fed"):
            if rd.get(k) not in (*DIRECTIONS, "neutral"):
                p.append(CardProblem(cid, "error", f"regime_dependency.{k} 非法: {rd.get(k)!r}"))
    elif "regime_dependency" in card:
        p.append(CardProblem(cid, "error", "regime_dependency 必须是映射"))

    proposed: set[str] = set()
    for pi in card.get("proposed_indicators") or []:
        if isinstance(pi, dict) and pi.get("id"):
            proposed.add(str(pi["id"]))
            for k in ("name", "source", "frequency"):
                if not pi.get(k):
                    p.append(CardProblem(cid, "warning", f"proposed_indicators.{pi['id']} 缺少 {k}"))

    ev = card.get("evidence_indicators") or []
    if not isinstance(ev, list):
        p.append(CardProblem(cid, "error", "evidence_indicators 必须是列表"))
    else:
        for i, e in enumerate(ev):
            if not isinstance(e, dict):
                p.append(CardProblem(cid, "error", f"evidence_indicators[{i}] 必须是映射"))
                continue
            iid = str(e.get("indicator_id", ""))
            if not iid:
                p.append(CardProblem(cid, "error", f"evidence_indicators[{i}] 缺少 indicator_id"))
            elif not _known_indicator(iid, registry, proposed):
                p.append(
                    CardProblem(
                        cid, "error", f"evidence_indicators[{i}]: 指标 {iid} 不在注册表也不在 proposed_indicators"
                    )
                )
            if e.get("expected_sign") not in SIGNS:
                p.append(CardProblem(cid, "error", f"evidence_indicators[{i}].expected_sign 非法"))
            if e.get("weight") not in WEIGHTS:
                p.append(CardProblem(cid, "warning", f"evidence_indicators[{i}].weight 非规范值"))
        if len(ev) < 2:
            p.append(CardProblem(cid, "warning", "证据指标少于 2 个"))

    vs = card.get("verification_signals") or []
    if isinstance(vs, list):
        if not 3 <= len(vs) <= 6:
            p.append(CardProblem(cid, "warning", f"验证信号应为 3 到 5 条，现有 {len(vs)}"))
        for i, v in enumerate(vs):
            if not isinstance(v, dict):
                p.append(CardProblem(cid, "error", f"verification_signals[{i}] 必须是映射"))
                continue
            if v.get("type") not in COND_TYPES:
                p.append(CardProblem(cid, "error", f"verification_signals[{i}].type 非法"))
            if v.get("type") == "quant":
                p += _validate_rule(v.get("rule"), cid, f"verification_signals[{i}]", registry, proposed)
            if "next_check" in v and not _is_date(v["next_check"]):
                p.append(CardProblem(cid, "error", f"verification_signals[{i}].next_check 不是 ISO 日期"))

    fc = card.get("falsification_conditions") or []
    if isinstance(fc, list):
        if not fc:
            p.append(CardProblem(cid, "error", "至少需要一条证伪条件"))
        for i, c in enumerate(fc):
            if not isinstance(c, dict):
                p.append(CardProblem(cid, "error", f"falsification_conditions[{i}] 必须是映射"))
                continue
            if c.get("type") not in COND_TYPES:
                p.append(CardProblem(cid, "error", f"falsification_conditions[{i}].type 非法"))
            if c.get("type") == "quant":
                p += _validate_rule(c.get("rule"), cid, f"falsification_conditions[{i}]", registry, proposed)
            if not _is_date(c.get("deadline")):
                p.append(CardProblem(cid, "error", f"falsification_conditions[{i}].deadline 不是 ISO 日期"))
            if not isinstance(c.get("version"), int):
                p.append(CardProblem(cid, "warning", f"falsification_conditions[{i}] 缺少整数 version"))
            if not _is_date(c.get("created")):
                p.append(CardProblem(cid, "warning", f"falsification_conditions[{i}] 缺少 created 日期"))

    nq = card.get("news_queries") or []
    if isinstance(nq, list) and not 3 <= len(nq) <= 6:
        p.append(CardProblem(cid, "warning", f"news_queries 应为 3 到 5 个，现有 {len(nq)}"))

    srcs = card.get("sources") or []
    if isinstance(srcs, list):
        primary = 0
        for i, s in enumerate(srcs):
            if not isinstance(s, dict):
                p.append(CardProblem(cid, "error", f"sources[{i}] 必须是映射"))
                continue
            if s.get("type") not in SOURCE_TYPES:
                p.append(CardProblem(cid, "warning", f"sources[{i}].type 非法"))
            if not str(s.get("url", "")).startswith("http"):
                p.append(CardProblem(cid, "warning", f"sources[{i}] 缺少 url"))
            if s.get("type") == "primary":
                primary += 1
        if primary < 3:
            p.append(CardProblem(cid, "warning", f"一手来源少于 3 个，现有 {primary}"))
    return p


def validate_collection(cards: dict[Path, dict[str, Any]], registry: Registry | None = None) -> list[CardProblem]:
    problems: list[CardProblem] = []
    ids: dict[str, Path] = {}
    for path, card in cards.items():
        problems += validate_card(card, registry, path)
        cid = card.get("id")
        if isinstance(cid, str):
            if cid in ids:
                problems.append(CardProblem(cid, "error", f"id 重复：{ids[cid].name} 与 {path.name}"))
            ids[cid] = path
    for card in cards.values():
        for t in card.get("tensions") or []:
            if isinstance(t, dict) and t.get("narrative_id") and t["narrative_id"] not in ids:
                problems.append(
                    CardProblem(str(card.get("id")), "warning", f"张力引用了不存在的叙事 {t['narrative_id']}")
                )
    return problems
