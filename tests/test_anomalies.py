from __future__ import annotations

from goldrising.rules.anomalies import flag_indicator


def test_jump_flag() -> None:
    flags = flag_indicator({"z_change_1d": 3.1, "pct_10y": 50.0, "staleness_days": 1}, "daily", 1)
    assert [f["code"] for f in flags] == ["jump"]
    assert "上行" in flags[0]["label"]


def test_extreme_flags() -> None:
    hi = flag_indicator({"z_change_1d": 0.1, "pct_10y": 97.0, "staleness_days": 0}, "daily", 0)
    lo = flag_indicator({"z_change_1d": 0.1, "pct_10y": None, "pct_5y": 2.0, "staleness_days": 0}, "daily", 0)
    assert hi[0]["code"] == "extreme_high"
    assert lo[0]["code"] == "extreme_low"


def test_stale_flag_respects_frequency() -> None:
    daily = flag_indicator({"z_change_1d": 0.0, "pct_10y": 50.0, "staleness_days": 9}, "daily", 1)
    weekly = flag_indicator({"z_change_1d": 0.0, "pct_10y": 50.0, "staleness_days": 9}, "weekly", 3)
    assert [f["code"] for f in daily] == ["stale"]
    assert weekly == []
