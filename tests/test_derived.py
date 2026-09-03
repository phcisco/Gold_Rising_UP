from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from goldrising.compute.derived import compute_derived
from goldrising.contracts import Derived, Indicator, Source


def _ind(op: str, inputs: tuple[str, ...], **params: object) -> Indicator:
    return Indicator(
        id="x",
        name="x",
        group="g",
        tier="2",
        unit="ratio",
        decimals=2,
        frequency="daily",
        lag_days=0,
        gold_sign=0,
        source=Source(provider="derived"),
        derived=Derived(op=op, inputs=inputs, params=dict(params)),
    )


def _s(values: list[float], start: str = "2024-01-01") -> pd.Series:
    return pd.Series(values, index=pd.bdate_range(start, periods=len(values)))


def test_sub_div_mul_align_on_dates() -> None:
    a = _s([10.0, 20.0, 30.0])
    b = _s([2.0, 4.0, 5.0])
    assert list(compute_derived(_ind("sub", ("a", "b")), {"a": a, "b": b})) == [8.0, 16.0, 25.0]
    assert list(compute_derived(_ind("div", ("a", "b")), {"a": a, "b": b})) == [5.0, 5.0, 6.0]
    assert list(compute_derived(_ind("mul", ("a", "b")), {"a": a, "b": b})) == [20.0, 80.0, 150.0]


def test_div_by_zero_dropped() -> None:
    a = _s([1.0, 2.0])
    b = _s([0.0, 2.0])
    out = compute_derived(_ind("div", ("a", "b")), {"a": a, "b": b})
    assert list(out) == [1.0]


def test_ffill_limited_alignment() -> None:
    a = _s([1.0] * 10)
    b = pd.Series([2.0], index=pd.bdate_range("2024-01-01", periods=1))
    out = compute_derived(_ind("sub", ("a", "b")), {"a": a, "b": b})
    # b 只向前填 5 个交易日
    assert out.shape[0] == 6


def test_ma_dist_and_mom() -> None:
    s = _s([100.0] * 20 + [110.0])
    ma = compute_derived(_ind("ma_dist", ("a",), window=20), {"a": s})
    assert round(float(ma.iloc[-1]), 4) == round((110 / 100.5 - 1) * 100, 4)
    mom = compute_derived(_ind("mom", ("a",), window=20), {"a": s})
    assert round(float(mom.iloc[-1]), 6) == 10.0


def test_pct_rank_rolling() -> None:
    s = _s(list(range(1, 61)))
    out = compute_derived(_ind("pct_rank", ("a",), window=40), {"a": s})
    assert round(float(out.iloc[-1]), 2) == 98.75


def test_beta_recovers_leverage() -> None:
    rng = np.random.default_rng(1)
    rb = rng.normal(0, 0.01, 200)
    b = 100 * np.cumprod(1 + rb)
    a = 100 * np.cumprod(1 + 2 * rb)
    out = compute_derived(_ind("beta", ("a", "b"), window=60), {"a": _s(list(a)), "b": _s(list(b))})
    assert abs(float(out.iloc[-1]) - 2.0) < 0.05


def test_lev_decay_zero_for_perfect_tracking_without_compounding() -> None:
    b = _s([100.0, 110.0, 121.0])
    a = _s([100.0, 130.0, 169.0])  # 3 倍日收益，路径损耗为正差
    out = compute_derived(_ind("lev_decay", ("a", "b"), window=2, leverage=3), {"a": a, "b": b})
    assert round(float(out.iloc[-1]), 6) == round(69.0 - 3 * 21.0, 6)


def test_missing_input_raises() -> None:
    with pytest.raises(KeyError):
        compute_derived(_ind("sub", ("a", "b")), {"a": _s([1.0])})
