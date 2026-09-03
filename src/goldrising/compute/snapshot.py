"""每日指标快照：把 curated 数据变成一份自描述的 JSON，供渲染与（第 2 阶段）AI 分析师使用。"""

from __future__ import annotations

import json
import logging
from datetime import UTC, date, datetime
from typing import Any

import pandas as pd

from goldrising.compute.derived import compute_derived
from goldrising.compute.stats import (
    changes,
    percentile_of_last,
    sparkline_points,
    staleness_days,
    zscore_of_last,
    zscore_of_last_change,
)
from goldrising.contracts import IndicatorSeries, Provenance, Registry
from goldrising.data.store import CuratedStore
from goldrising.rules.anomalies import flag_indicator
from goldrising.workspace import Workspace

log = logging.getLogger(__name__)

OBS_PER_YEAR = {"daily": 252, "weekly": 52, "monthly": 12, "quarterly": 4}


def compute_derived_all(registry: Registry, store: CuratedStore) -> list[str]:
    """按拓扑顺序计算全部派生指标并入库。返回失败列表。"""
    failures: list[str] = []
    for ind in registry.derived_in_order():
        assert ind.derived is not None
        inputs: dict[str, pd.Series] = {}
        ok = True
        for dep in ind.derived.inputs:
            s = store.load(dep)
            if s is None or s.values.empty:
                failures.append(f"{ind.id}: 缺少输入 {dep}")
                ok = False
                break
            inputs[dep] = s.values
        if not ok:
            continue
        try:
            values = compute_derived(ind, inputs)
        except Exception as e:
            failures.append(f"{ind.id}: {type(e).__name__}: {e}")
            continue
        if values.empty:
            failures.append(f"{ind.id}: 结果为空")
            continue
        deps = [store.load(d) for d in ind.derived.inputs]
        prov = Provenance(
            provider="derived",
            publisher="派生自 " + "、".join(ind.derived.inputs),
            series=f"{ind.derived.op}({', '.join(ind.derived.inputs)})",
            url="",
            fetched_at=Provenance.now_iso(),
            as_of=values.index[-1].strftime("%Y-%m-%d"),
            lag_days=ind.lag_days,
            note="; ".join(f"{d.indicator_id}@{d.provenance.as_of}" for d in deps if d is not None),
        )
        store.save(IndicatorSeries(ind.id, values, prov), merge=False)
    return failures


def _entry(ind_id: str, registry: Registry, series: IndicatorSeries, today: date) -> dict[str, Any]:
    ind = registry.by_id(ind_id)
    v = series.values
    per_year = OBS_PER_YEAR.get(ind.frequency, 252)
    weekly = ind.frequency != "daily"
    entry: dict[str, Any] = {
        "id": ind.id,
        "name": ind.name,
        "group": ind.group,
        "tier": ind.tier,
        "unit": ind.unit,
        "decimals": ind.decimals,
        "frequency": ind.frequency,
        "lag_days": ind.lag_days,
        "gold_sign": ind.gold_sign,
        "note": ind.note,
        "last": series.last_value,
        "last_date": series.last_date.isoformat() if series.last_date else None,
        "staleness_days": staleness_days(series.last_date, today),
        "changes": changes(v, frequency=ind.frequency),
        # 窗口分位只在历史覆盖该窗口至少 80% 时给出，避免把 3 年历史标成"10 年分位"
        "pct_1y": percentile_of_last(v, window=per_year, min_obs=max(30, int(per_year * 0.8))),
        "pct_5y": percentile_of_last(v, window=per_year * 5, min_obs=max(30, int(per_year * 5 * 0.8))),
        "pct_10y": percentile_of_last(v, window=per_year * 10, min_obs=max(30, int(per_year * 10 * 0.8))),
        "pct_all": percentile_of_last(v, window=None),
        "z_250": zscore_of_last(v, window=per_year),
        "z_change_1d": zscore_of_last_change(v, window=per_year),
        "sparkline": sparkline_points(v, n=120 if not weekly else 104),
        "provenance": series.provenance.to_dict(),
        "observations": int(v.shape[0]),
        "first_date": v.index[0].strftime("%Y-%m-%d") if not v.empty else None,
    }
    entry["flags"] = flag_indicator(entry, ind.frequency, ind.lag_days)
    return entry


def build_snapshot(
    workspace: Workspace,
    registry: Registry,
    today: date | None = None,
    fetch_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    today = today or datetime.now(UTC).date()
    store = CuratedStore(workspace.data_curated)
    derived_failures = compute_derived_all(registry, store)
    indicators: dict[str, Any] = {}
    missing: list[str] = []
    for ind in registry.indicators:
        s = store.load(ind.id)
        if s is None or s.values.empty:
            missing.append(ind.id)
            continue
        indicators[ind.id] = _entry(ind.id, registry, s, today)
    fed_details: dict[str, Any] | None = None
    fed_path = workspace.data_curated / "ff_path.details.json"
    if fed_path.exists():
        fed_details = json.loads(fed_path.read_text(encoding="utf-8"))
    snapshot: dict[str, Any] = {
        "run_date": today.isoformat(),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "registry_version": registry.version,
        "groups": [
            {"id": g.id, "name": g.name, "order": g.order, "question": g.question}
            for g in sorted(registry.groups, key=lambda g: g.order)
        ],
        "indicators": indicators,
        "missing": missing,
        "derived_failures": derived_failures,
        "fedwatch": fed_details,
        "fetch_report": fetch_report,
    }
    workspace.snapshots_dir.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(snapshot, ensure_ascii=False, indent=1)
    (workspace.snapshots_dir / f"{today.isoformat()}.json").write_text(payload, encoding="utf-8")
    (workspace.snapshots_dir / "latest.json").write_text(payload, encoding="utf-8")
    if derived_failures:
        log.warning("派生指标失败: %s", derived_failures)
    return snapshot
