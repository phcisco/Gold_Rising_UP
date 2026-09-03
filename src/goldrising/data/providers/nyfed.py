"""纽约联储：参考利率 API（EFFR）与 ACM 期限溢价模型（xls）。一手来源。"""

from __future__ import annotations

import io
from datetime import date, timedelta
from typing import Any

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

SEARCH = "https://markets.newyorkfed.org/api/rates/unsecured/{code}/search.json"
LAST = "https://markets.newyorkfed.org/api/rates/unsecured/{code}/last/{n}.json"
ACM_URL = "https://www.newyorkfed.org/medialibrary/media/research/data_indicators/ACMTermPremium.xls"


def pick_acm_series(sheets: dict[str, pd.DataFrame], column: str) -> pd.Series:
    """从 ACM 工作簿中选出含 DATE 与目标列、行数最多的工作表（日频表），返回日期索引序列。"""
    best: pd.Series | None = None
    for df in sheets.values():
        cols = {str(c).strip().upper(): c for c in df.columns}
        if "DATE" not in cols or column.upper() not in cols:
            continue
        dates = pd.to_datetime(df[cols["DATE"]], errors="coerce")
        values = pd.to_numeric(df[cols[column.upper()]], errors="coerce")
        s = pd.Series(values.to_numpy(), index=pd.DatetimeIndex(dates)).dropna().sort_index()
        s = s[pd.notna(s.index)]
        if best is None or s.shape[0] > best.shape[0]:
            best = s
    if best is None or best.empty:
        raise ProviderError(f"ACM 工作簿中找不到列 {column}")
    return best


def load_acm(ctx: FetchContext, column: str) -> pd.Series:
    key = f"nyfed:acm:{column}"
    cached = ctx.cache.get(key)
    if isinstance(cached, pd.Series):
        return cached
    sheets = ctx.cache.get("nyfed:acm:sheets")
    if not isinstance(sheets, dict):
        resp = ctx.get(ACM_URL, raw_name="nyfed/ACMTermPremium.xls")
        sheets = pd.read_excel(io.BytesIO(resp.content), sheet_name=None, engine="xlrd")
        ctx.cache["nyfed:acm:sheets"] = sheets
    s = pick_acm_series(sheets, column)
    ctx.cache[key] = s
    return s


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
        series = indicator.source.series
        if series.lower() == "effr":
            s = load_effr(ctx, since)
            label = "EFFR"
        elif series.lower().startswith("acm:"):
            column = series.split(":", 1)[1]
            s = load_acm(ctx, column)
            label = f"ACM {column}"
        else:
            raise ProviderError(f"{indicator.id}: nyfed 只支持 effr 或 acm:<列名>")
        prov = Provenance(
            provider=self.name,
            publisher=indicator.source.publisher or "Federal Reserve Bank of New York",
            series=label,
            url=indicator.source.url,
            fetched_at=Provenance.now_iso(),
            as_of=s.index[-1].strftime("%Y-%m-%d"),
            lag_days=indicator.lag_days,
        )
        return IndicatorSeries(indicator.id, s, prov)
