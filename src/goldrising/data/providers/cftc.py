"""CFTC 公开报告环境（Socrata）：分类报告 Disaggregated Futures Only。一手来源。"""

from __future__ import annotations

from datetime import date

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

URL = "https://publicreporting.cftc.gov/resource/72hh-3qpy.json"
GOLD_CODE = "088691"


def load_gold_disagg(ctx: FetchContext) -> pd.DataFrame:
    key = "cftc:gold_disagg"
    cached = ctx.cache.get(key)
    if isinstance(cached, pd.DataFrame):
        return cached
    params = {
        "$where": f"cftc_contract_market_code='{GOLD_CODE}'",
        "$select": "report_date_as_yyyy_mm_dd,m_money_positions_long_all,m_money_positions_short_all,open_interest_all",
        "$order": "report_date_as_yyyy_mm_dd ASC",
        "$limit": "5000",
    }
    resp = ctx.get(URL, params=params, raw_name="cftc/gold_disagg.json")
    rows = resp.json()
    if not rows:
        raise ProviderError("CFTC 返回空")
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"])
    for c in ("m_money_positions_long_all", "m_money_positions_short_all", "open_interest_all"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.set_index("date").sort_index()
    ctx.cache[key] = df
    return df


class CftcProvider:
    name = "cftc"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        df = load_gold_disagg(ctx)
        series = indicator.source.series
        if series == "mm_net":
            s = df["m_money_positions_long_all"] - df["m_money_positions_short_all"]
        elif series == "oi":
            s = df["open_interest_all"]
        else:
            raise ProviderError(f"{indicator.id}: 未知 CFTC 序列 {series}")
        s = s.dropna()
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "U.S. Commodity Futures Trading Commission",
            series=f"Disaggregated Futures Only / GOLD ({GOLD_CODE}) / {series}",
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
            note="周二持仓，周五 15:30 ET 发布",
        )
        return IndicatorSeries(indicator.id, s, prov)
