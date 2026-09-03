from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

import pandas as pd

from goldrising.data.providers.yahoo import contract_ticker, drop_incomplete_bars, gc_active_contracts

NY = ZoneInfo("America/New_York")


def _s(dates: list[str]) -> pd.Series:
    return pd.Series([1.0] * len(dates), index=pd.to_datetime(dates))


def test_drops_today_bar_before_close() -> None:
    s = _s(["2026-09-01", "2026-09-02", "2026-09-03"])
    out = drop_incomplete_bars(s, datetime(2026, 9, 3, 1, 30, tzinfo=NY))
    assert list(out.index.strftime("%Y-%m-%d")) == ["2026-09-01", "2026-09-02"]


def test_keeps_today_bar_after_close_and_drops_future() -> None:
    s = _s(["2026-09-02", "2026-09-03", "2026-09-04"])
    out = drop_incomplete_bars(s, datetime(2026, 9, 3, 18, 0, tzinfo=NY))
    assert list(out.index.strftime("%Y-%m-%d")) == ["2026-09-02", "2026-09-03"]


def test_gc_active_contracts_roll_rule() -> None:
    assert gc_active_contracts(date(2026, 9, 3)) == [(2026, 12), (2027, 2)]
    assert gc_active_contracts(date(2026, 12, 10)) == [(2026, 12), (2027, 2)]
    assert gc_active_contracts(date(2026, 12, 25)) == [(2027, 2), (2027, 4)]
    assert contract_ticker("GC", 2026, 12, "CMX") == "GCZ26.CMX"
    assert contract_ticker("ZQ", 2027, 1, "CBT") == "ZQF27.CBT"
