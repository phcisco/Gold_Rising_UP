from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from goldrising.compute.stats import (
    changes,
    percentile_of_last,
    sparkline_points,
    staleness_days,
    zscore_of_last,
    zscore_of_last_change,
)


def _series(values: list[float]) -> pd.Series:
    idx = pd.bdate_range("2024-01-01", periods=len(values))
    return pd.Series(values, index=idx)


def test_percentile_of_last_is_midrank() -> None:
    s = _series(list(range(1, 101)))  # 1..100，最新值 100
    assert percentile_of_last(s) == 99.5
    s2 = _series(list(range(100, 0, -1)))  # 最新值 1
    assert percentile_of_last(s2) == 0.5


def test_percentile_requires_min_obs() -> None:
    assert percentile_of_last(_series([1.0, 2.0, 3.0])) is None


def test_percentile_window_limits_history() -> None:
    s = _series([1000.0] * 50 + list(range(1, 51)))
    assert percentile_of_last(s, window=50) == 99.0
    full = percentile_of_last(s)
    assert full is not None and full < 60


def test_zscore_of_last() -> None:
    rng = np.random.default_rng(0)
    base = rng.normal(0, 1, 300)
    base[-1] = 10.0
    z = zscore_of_last(_series(list(base)), window=250)
    assert z is not None and z > 5


def test_zscore_of_change() -> None:
    vals = list(np.linspace(0, 10, 300))
    vals[-1] = vals[-2] + 5.0
    z = zscore_of_last_change(_series(vals), window=250)
    assert z is not None and z > 10


def test_changes_daily_and_weekly() -> None:
    s = _series([100.0 + i for i in range(300)])
    c = changes(s)
    assert c["1d"]["abs"] == 1.0
    assert c["20d"]["abs"] == 20.0
    assert round(c["250d"]["pct"] or 0, 4) == round(250 / 149 * 100, 4)
    w = changes(s, weekly=True)
    assert w["20d"]["abs"] == 4.0


def test_changes_insufficient_history() -> None:
    c = changes(_series([1.0, 2.0]))
    assert c["20d"]["abs"] is None


def test_staleness_and_sparkline() -> None:
    assert staleness_days(date(2026, 9, 1), date(2026, 9, 3)) == 2
    assert staleness_days(None, date(2026, 9, 3)) is None
    pts = sparkline_points(_series([1.0, 2.0, 3.0]), n=2)
    assert len(pts) == 2 and pts[-1][1] == 3.0


def test_percentile_window_needs_coverage() -> None:
    s = _series(list(range(1, 787)))  # 约 3 年日频
    assert percentile_of_last(s, window=2520, min_obs=int(2520 * 0.8)) is None
    assert percentile_of_last(s, window=252, min_obs=int(252 * 0.8)) is not None
