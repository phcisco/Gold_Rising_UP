"""Yahoo Finance v8 图表接口：连续行情与期货各月合约。交易所数据的分发商，非官方结算价。"""

from __future__ import annotations

from datetime import UTC, date, datetime, time
from urllib.parse import quote
from zoneinfo import ZoneInfo

import pandas as pd

from goldrising.contracts import Indicator, IndicatorSeries, Provenance
from goldrising.data.providers.base import FetchContext, ProviderError

CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
SESSION_CLOSE_LOCAL = time(17, 15)  # 交易所本地时间；此前的"今日" bar 视为未收盘


def drop_incomplete_bars(s: pd.Series, now_local: datetime) -> pd.Series:
    """只保留已完成的交易日：剔除晚于本地今日的 bar；本地今日 bar 仅在收盘后保留。"""
    today = pd.Timestamp(now_local.date())
    s = s[s.index <= today]
    if not s.empty and s.index[-1] == today and now_local.time() < SESSION_CLOSE_LOCAL:
        s = s.iloc[:-1]
    return s


MONTH_CODES = {1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M", 7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z"}
GC_ACTIVE_MONTHS = (2, 4, 6, 8, 12)


def fetch_symbol_history(ctx: FetchContext, symbol: str, range_: str = "10y") -> pd.Series:
    key = f"yahoo:{symbol}:{range_}"
    cached = ctx.cache.get(key)
    if isinstance(cached, pd.Series):
        return cached
    url = CHART.format(symbol=quote(symbol, safe=""))
    resp = ctx.get(url, params={"range": range_, "interval": "1d", "events": "div,splits"}, timeout=30)
    data = resp.json()
    chart = data.get("chart", {})
    result = chart.get("result")
    if not result:
        raise ProviderError(f"Yahoo 无结果 {symbol}: {chart.get('error')}")
    r0 = result[0]
    stamps = r0.get("timestamp") or []
    closes = (r0.get("indicators", {}).get("quote") or [{}])[0].get("close") or []
    tzname = r0.get("meta", {}).get("exchangeTimezoneName") or "UTC"
    tz = ZoneInfo(tzname)
    dates = []
    vals = []
    for ts, c in zip(stamps, closes, strict=False):
        if c is None:
            continue
        d = datetime.fromtimestamp(int(ts), tz=UTC).astimezone(tz).date()
        dates.append(pd.Timestamp(d))
        vals.append(float(c))
    if not vals:
        raise ProviderError(f"Yahoo 返回空序列 {symbol}")
    s = pd.Series(vals, index=pd.DatetimeIndex(dates)).sort_index()
    s = s[~s.index.duplicated(keep="last")]
    s = drop_incomplete_bars(s, datetime.now(tz))
    if s.empty:
        raise ProviderError(f"Yahoo 无已完成交易日 {symbol}")
    ctx.cache[key] = s
    return s


def _provenance(indicator: Indicator, symbol: str, s: pd.Series, note: str = "") -> Provenance:
    return Provenance(
        provider="yahoo",
        publisher=indicator.source.publisher or "Yahoo Finance",
        series=symbol,
        url=indicator.source.url or f"https://finance.yahoo.com/quote/{quote(symbol, safe='')}",
        fetched_at=Provenance.now_iso(),
        as_of=s.index[-1].strftime("%Y-%m-%d"),
        lag_days=indicator.lag_days,
        note=note or "连续报价（收盘），非交易所官方结算价",
    )


class YahooProvider:
    name = "yahoo"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        symbol = indicator.source.symbol
        if not symbol:
            raise ProviderError(f"{indicator.id}: yahoo 需要 symbol")
        s = fetch_symbol_history(ctx, symbol)
        return IndicatorSeries(indicator.id, s, _provenance(indicator, symbol, s))


def gc_active_contracts(today: date, count: int = 2, roll_day: int = 20) -> list[tuple[int, int]]:
    """返回最近 count 个活跃 COMEX 黄金合约的 (年, 月)。当月为活跃月且已过 roll_day 则跳过。"""
    out: list[tuple[int, int]] = []
    y, m = today.year, today.month
    while len(out) < count:
        if (
            m in GC_ACTIVE_MONTHS
            and not (y == today.year and m == today.month and today.day > roll_day)
            and ((y, m) >= (today.year, today.month))
        ):
            out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def contract_ticker(root: str, year: int, month: int, suffix: str) -> str:
    return f"{root}{MONTH_CODES[month]}{year % 100:02d}.{suffix}"


class YahooGoldContractProvider:
    name = "yahoo_gc_contract"

    def fetch(self, indicator: Indicator, ctx: FetchContext, since: date | None = None) -> IndicatorSeries:
        position = int(indicator.source.params.get("position", 1))
        contracts = gc_active_contracts(ctx.today, count=max(position, 2))
        year, month = contracts[position - 1]
        symbol = contract_ticker("GC", year, month, "CMX")
        s = fetch_symbol_history(ctx, symbol, range_="2y")
        prov = _provenance(indicator, symbol, s, note=f"活跃合约 {year}-{month:02d}，按 20 日换月规则选取")
        return IndicatorSeries(indicator.id, s, prov)
