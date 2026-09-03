"""纽约联储参考利率 API（EFFR）。一手来源。"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

SEARCH = "https://markets.newyorkfed.org/api/rates/unsecured/{code}/search.json"
LAST = "https://markets.newyorkfed.org/api/rates/unsecured/{code}/last/{n}.json"


def load_effr(ctx: FetchContext, since: date | None = None) -> pd.Series:
    key = "nyfed:effr"
    cached = ctx.cache.get(key)
    if isinstance(cached, pd.Series):
        return cached
    start = since or (ctx.today - timedelta(days=365 * 10))
    rows: list[dict[str, Any]] = []
    try:
        resp = ctx.get(
            SEARCH.format(code="effr"),
            params={"startDate": start.isoformat(), "endDate": ctx.today.isoformat()},
            raw_name="nyfed/effr_search.json",
        )
        rows = list(resp.json().get("refRates", []))
    except ProviderError:
        rows = []
    if not rows:
        resp = ctx.get(LAST.format(code="effr", n=500), raw_name="nyfed/effr_last500.json")
        rows = list(resp.json().get("refRates", []))
    if not rows:
        raise ProviderError("纽约联储 EFFR 返回空")
    idx = pd.to_datetime([r["effectiveDate"] for r in rows])
    s = pd.Series([float(r["percentRate"]) for r in rows], index=idx).sort_index()
    ctx.cache[key] = s
    return s


class NYFedProvider:
    name = "nyfed"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        if indicator.source.series.lower() != "effr":
            raise ProviderError(f"{indicator.id}: nyfed 目前只支持 effr")
        s = load_effr(ctx, since)
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "Federal Reserve Bank of New York",
            series="EFFR",
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
        )
        return IndicatorSeries(indicator.id, s, prov)
