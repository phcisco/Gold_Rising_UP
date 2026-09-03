"""Cboe 指数历史数据（VIX、GVZ）。一手来源。"""

from __future__ import annotations

import io
from datetime import date

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

URL = "https://cdn.cboe.com/api/global/us_indices/daily_prices/{series}_History.csv"


class CboeProvider:
    name = "cboe"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        series = indicator.source.series.upper()
        resp = ctx.get(URL.format(series=series), raw_name=f"cboe/{series}_History.csv")
        df = pd.read_csv(io.StringIO(resp.text))
        cols = {c.upper(): c for c in df.columns}
        if "DATE" not in cols:
            raise ProviderError(f"{indicator.id}: Cboe CSV 缺少 DATE 列")
        value_col = cols.get("CLOSE") or cols.get(series) or next(c for c in df.columns if c != cols["DATE"])
        dates = pd.to_datetime(df[cols["DATE"]], errors="coerce")
        values = pd.to_numeric(df[value_col], errors="coerce")
        s = pd.Series(values.to_numpy(), index=pd.DatetimeIndex(dates)).dropna()
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "Cboe Global Markets",
            series=series,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
        )
        return IndicatorSeries(indicator.id, s, prov)
