"""人工维护的 CSV（data/manual/<series>.csv，列 date,value）。用于尚无自动接口的低频官方数据。"""

from __future__ import annotations

from datetime import date

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError


class ManualProvider:
    name = "manual"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        path = ctx.workspace.data_manual / f"{indicator.source.series}.csv"
        if not path.exists():
            raise ProviderError(f"{indicator.id}: 缺少人工数据文件 {path.name}")
        df = pd.read_csv(path, parse_dates=["date"])
        s = pd.Series(
            pd.to_numeric(df["value"], errors="coerce").to_numpy(), index=pd.DatetimeIndex(df["date"])
        ).dropna()
        if s.empty:
            raise ProviderError(f"{indicator.id}: 人工数据文件为空")
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher,
            series=indicator.source.series,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
            note="人工录入的官方发布值",
        )
        return IndicatorSeries(indicator.id, s, prov)
