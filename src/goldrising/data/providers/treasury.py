"""美国财政部每日收益率曲线（名义与实际）。一手来源。"""

from __future__ import annotations

import io
from datetime import date

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

BASE = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/{year}/all"
TYPES = {"nominal": "daily_treasury_yield_curve", "real": "daily_treasury_real_yield_curve"}
HISTORY_YEARS = 10


class TreasuryProvider:
    name = "treasury"

    def _year_frame(self, ctx: FetchContext, kind: str, year: int) -> pd.DataFrame:
        key = f"treasury:{kind}:{year}"
        cached = ctx.cache.get(key)
        if isinstance(cached, pd.DataFrame):
            return cached
        tdr_type = TYPES[kind]
        params = {"type": tdr_type, "field_tdr_date_value": str(year), "page": "", "_format": "csv"}
        resp = ctx.get(BASE.format(year=year), params=params, raw_name=f"treasury/{kind}_{year}.csv")
        df = pd.read_csv(io.StringIO(resp.text))
        if "Date" not in df.columns:
            raise ProviderError(f"财政部 CSV 缺少 Date 列: {kind} {year}")
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
        df = df.dropna(subset=["Date"]).set_index("Date").sort_index()
        ctx.cache[key] = df
        return df

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        try:
            kind, column = indicator.source.series.split(":", 1)
        except ValueError as e:
            raise ProviderError(f"{indicator.id}: series 需为 'nominal:<列名>' 或 'real:<列名>'") from e
        if kind not in TYPES:
            raise ProviderError(f"{indicator.id}: 未知曲线类型 {kind}")
        start_year = since.year if since else ctx.today.year - HISTORY_YEARS
        frames = []
        for year in range(start_year, ctx.today.year + 1):
            try:
                frames.append(self._year_frame(ctx, kind, year))
            except ProviderError:
                if year == ctx.today.year:
                    raise
        if not frames:
            raise ProviderError(f"{indicator.id}: 无数据")
        df = pd.concat(frames).sort_index()
        if column not in df.columns:
            raise ProviderError(f"{indicator.id}: 财政部 CSV 无列 {column}，现有列 {list(df.columns)}")
        values = pd.to_numeric(df[column], errors="coerce").dropna()
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "U.S. Department of the Treasury",
            series=indicator.source.series,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=values.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
            note="Daily Treasury Par Yield Curve Rates / Real Yield Curve Rates",
        )
        return IndicatorSeries(indicator.id, values, prov)
