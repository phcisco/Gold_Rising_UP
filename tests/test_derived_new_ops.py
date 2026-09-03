from __future__ import annotations

import numpy as np
import pandas as pd

from goldrising.compute.derived import compute_derived
from goldrising.compute.stats import changes
from goldrising.contracts import Derived, Indicator, Source
from goldrising.data.providers.nyfed import pick_acm_series


def _ind(op: str, inputs: list[str], **params: object) -> Indicator:
    return Indicator(
        id="x",
        name="x",
        group="g",
        tier="3",
        unit="ratio",
        decimals=2,
        frequency="daily",
        lag_days=0,
        gold_sign=0,
        source=Source(provider="derived"),
        derived=Derived(op=op, inputs=tuple(inputs), params=dict(params)),
    )


def test_yoy_on_monthly_series() -> None:
    idx = pd.date_range("2020-01-31", periods=30, freq="ME")
    s = pd.Series(100.0 * (1.03 ** (np.arange(30) / 12.0)), index=idx)
    out = compute_derived(_ind("yoy", ["a"], periods=12), {"a": s})
    assert out.shape[0] == 18
    assert abs(out.iloc[-1] - 3.0) < 1e-6


def test_rolling_corr_of_inverse_series_is_minus_one() -> None:
    idx = pd.bdate_range("2024-01-01", periods=200)
    rng = np.random.default_rng(0)
    a = pd.Series(100 + rng.normal(0, 1, 200).cumsum(), index=idx)
    b = 1.0 / a
    out = compute_derived(_ind("rolling_corr", ["a", "b"], window=60), {"a": a, "b": b})
    assert out.shape[0] == 200 - 60
    assert out.iloc[-1] < -0.95


def test_realized_vol_matches_manual() -> None:
    idx = pd.bdate_range("2024-01-01", periods=60)
    rng = np.random.default_rng(1)
    s = pd.Series(100 * np.exp(rng.normal(0, 0.01, 60).cumsum()), index=idx)
    out = compute_derived(_ind("realized_vol", ["a"], window=20, per_year=252), {"a": s})
    manual = float(np.log(s / s.shift(1)).iloc[-20:].std(ddof=1) * np.sqrt(252) * 100)
    assert abs(out.iloc[-1] - manual) < 1e-9


def test_changes_uses_monthly_horizons() -> None:
    idx = pd.date_range("2020-01-31", periods=30, freq="ME")
    s = pd.Series(np.arange(30, dtype=float), index=idx)
    out = changes(s, frequency="monthly")
    assert out["250d"]["abs"] == 12.0
    assert out["60d"]["abs"] == 3.0


def test_pick_acm_series_prefers_daily_sheet() -> None:
    monthly = pd.DataFrame({"DATE": ["31-Jan-2026", "28-Feb-2026"], "ACMTP10": [0.5, 0.6]})
    daily = pd.DataFrame(
        {
            "DATE": pd.bdate_range("2026-01-01", periods=5),
            "ACMTP10": [0.7, 0.71, 0.72, 0.73, 0.74],
            "ACMRNY10": [4.0] * 5,
        }
    )
    s = pick_acm_series({"ACM Monthly": monthly, "ACM Daily": daily}, "ACMTP10")
    assert s.shape[0] == 5
    assert abs(s.iloc[-1] - 0.74) < 1e-12
