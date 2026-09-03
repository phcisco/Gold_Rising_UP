"""FRED API。需要 FRED_API_KEY（本机直连 fredgraph CSV 被拦截，只能走 API）。"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

URL = "https://api.stlouisfed.org/fred/series/observations"


class FredProvider:
    name = "fred"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        key = ctx.env.get("FRED_API_KEY", "").strip()
        if not key:
            raise ProviderError(f"{indicator.id}: 缺少 FRED_API_KEY，跳过")
        start = since or (ctx.today - timedelta(days=365 * 10))
        params = {
            "series_id": indicator.source.series,
            "api_key": key,
            "file_type": "json",
            "observation_start": start.isoformat(),
        }
        resp = ctx.get(URL, params=params)  # 不落 raw：URL 含密钥
        obs = resp.json().get("observations", [])
        if not obs:
            raise ProviderError(f"{indicator.id}: FRED 返回空")
        idx = pd.to_datetime([o["date"] for o in obs])
        vals = pd.to_numeric(pd.Series([o["value"] for o in obs]), errors="coerce")
        s = pd.Series(vals.to_numpy(), index=idx).dropna()
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "Federal Reserve Bank of St. Louis (FRED)",
            series=indicator.source.series,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
        )
        return IndicatorSeries(indicator.id, s, prov)
