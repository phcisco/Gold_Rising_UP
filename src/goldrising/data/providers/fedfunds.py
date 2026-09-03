"""按 CME FedWatch 公开方法，用 30 天联邦基金期货各月合约复算 FOMC 隐含路径。"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

from goldrising.compute.fedwatch import MeetingStep, compute_path
from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError
from goldrising.data.providers.nyfed import load_effr
from goldrising.data.providers.yahoo import contract_ticker, fetch_symbol_history

HORIZON_MONTHS = 14
HISTORY_DAYS = 300


def load_fomc_dates(path: Path) -> list[date]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    dates = [pd.Timestamp(d).date() for d in data.get("decision_dates", [])]
    return sorted(dates)


def _contract_months(today: date, horizon: int) -> list[tuple[int, int]]:
    out = []
    y, m = today.year, today.month
    for _ in range(horizon):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def _load_contract_frame(ctx: FetchContext) -> pd.DataFrame:
    key = "fedfunds:frame"
    cached = ctx.cache.get(key)
    if isinstance(cached, pd.DataFrame):
        return cached
    cols: dict[str, pd.Series] = {}
    failures: list[str] = []
    for y, m in _contract_months(ctx.today, HORIZON_MONTHS):
        sym = contract_ticker("ZQ", y, m, "CBT")
        try:
            cols[f"{y}-{m:02d}"] = fetch_symbol_history(ctx, sym, range_="2y")
        except ProviderError as e:
            failures.append(f"{sym}: {e}")
    if len(cols) < 6:
        raise ProviderError(f"联邦基金期货合约不足（{len(cols)} 个）: {failures[:3]}")
    frame = pd.concat(cols, axis=1).sort_index().ffill(limit=5)
    frame.attrs["failures"] = failures
    ctx.cache[key] = frame
    return frame


def _steps_to_json(asof: date, effr: float, steps: list[MeetingStep]) -> dict[str, object]:
    return {
        "as_of": asof.isoformat(),
        "effr": effr,
        "method": "CME FedWatch 公开方法复算：合约隐含月均利率 = 100 - 价格；含会议月份按会前/会后天数拆分；"
        "会后月份若无会议则直接取其合约；变动按 25bp 一档拆为两种结果的概率。",
        "meetings": [s.to_dict() for s in steps],
    }


class FedFundsProvider:
    name = "fedfunds"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        series = indicator.source.series
        if series not in {"next_change_bp", "cum_change_bp"}:
            raise ProviderError(f"{indicator.id}: 未知 fedfunds 序列 {series}")
        meetings = load_fomc_dates(ctx.workspace.data_manual / "fomc_calendar.yaml")
        frame = _load_contract_frame(ctx)
        effr = load_effr(ctx)
        effr_aligned = effr.reindex(frame.index.union(effr.index)).ffill().reindex(frame.index)
        dates = frame.index[-HISTORY_DAYS:]
        next_vals: list[float] = []
        cum_vals: list[float] = []
        kept: list[pd.Timestamp] = []
        latest_steps: list[MeetingStep] = []
        latest_asof: date | None = None
        latest_effr = float("nan")
        for ts in dates:
            row = frame.loc[ts].dropna()
            e = effr_aligned.get(ts)
            if row.empty or e is None or pd.isna(e):
                continue
            rates = {(int(k[:4]), int(k[5:7])): 100.0 - float(v) for k, v in row.items()}
            asof = ts.date()
            steps = compute_path(asof, rates, float(e), meetings)
            if not steps:
                continue
            kept.append(ts)
            next_vals.append(steps[0].change_bp)
            horizon_steps = [s for s in steps if (s.date - asof).days <= 366]
            cum_vals.append(horizon_steps[-1].cum_change_bp if horizon_steps else steps[-1].cum_change_bp)
            latest_steps, latest_asof, latest_effr = steps, asof, float(e)
        if not kept:
            raise ProviderError("无法计算联邦基金隐含路径")
        if latest_asof is not None:
            out = ctx.workspace.data_curated / "ff_path.details.json"
            out.write_text(
                json.dumps(_steps_to_json(latest_asof, latest_effr, latest_steps), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        values = pd.Series(next_vals if series == "next_change_bp" else cum_vals, index=pd.DatetimeIndex(kept))
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "CME Group 30-Day Fed Funds futures via Yahoo Finance",
            series=series,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=values.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
            note="复算值；合约缺失: " + "; ".join(frame.attrs.get("failures", [])[:3]),
            extra={"contracts": list(frame.columns)},
        )
        return IndicatorSeries(indicator.id, values, prov)
