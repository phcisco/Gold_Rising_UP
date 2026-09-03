from __future__ import annotations

from datetime import date

from goldrising.compute.fedwatch import compute_path, step_probabilities


def test_step_probabilities_split_between_adjacent_steps() -> None:
    assert step_probabilities(0.0) == {"0": 1.0}
    assert step_probabilities(-25.0) == {"-25": 1.0}
    p = step_probabilities(-12.5)
    assert p == {"-25": 0.5, "0": 0.5}
    p2 = step_probabilities(-30.0)
    assert p2["-50"] == 0.2 and p2["-25"] == 0.8


def test_compute_path_uses_next_month_when_no_meeting() -> None:
    asof = date(2026, 9, 3)
    meetings = [date(2026, 9, 16), date(2026, 11, 18)]
    effr = 3.63
    # 9 月会议后降 25bp 至 3.38：10 月无会议，合约直接给出会后利率
    sep_avg = (3.63 * 16 + 3.38 * 14) / 30
    rates = {(2026, 9): sep_avg, (2026, 10): 3.38, (2026, 11): 3.30, (2026, 12): 3.13}
    steps = compute_path(asof, rates, effr, meetings)
    assert len(steps) == 2
    s1, s2 = steps
    assert s1.method == "next_month"
    assert abs(s1.change_bp + 25.0) < 1e-6
    assert s1.probabilities == {"-25": 1.0}
    assert s2.method == "next_month"
    assert abs(s2.post_rate - 3.13) < 1e-9
    assert abs(s2.cum_change_bp - (3.13 - 3.63) * 100) < 1e-6


def test_compute_path_intra_month_when_next_month_has_meeting() -> None:
    asof = date(2026, 11, 20)
    meetings = [date(2026, 12, 9), date(2027, 1, 27)]
    effr = 3.38
    # 12 月 9 日会议降 25bp：12 月 31 天，9 天会前 3.38，22 天会后 3.13
    dec_avg = (3.38 * 9 + 3.13 * 22) / 31
    rates = {(2026, 11): 3.38, (2026, 12): dec_avg, (2027, 1): 3.13}
    steps = compute_path(asof, rates, effr, meetings)
    assert steps[0].method == "intra_month"
    assert abs(steps[0].post_rate - 3.13) < 1e-9
    assert abs(steps[0].change_bp + 25.0) < 1e-6


def test_compute_path_stops_when_contracts_missing() -> None:
    steps = compute_path(date(2026, 9, 3), {(2026, 9): 3.6}, 3.63, [date(2026, 9, 16), date(2026, 10, 28)])
    # 9 月会议：10 月有会议且 9 月可月内拆分 → 1 步；10 月无合约 → 停止
    assert len(steps) == 1 and steps[0].method == "intra_month"


def test_compute_path_ignores_past_meetings() -> None:
    steps = compute_path(
        date(2026, 9, 20), {(2026, 10): 3.5, (2026, 11): 3.4}, 3.63, [date(2026, 9, 16), date(2026, 10, 28)]
    )
    assert len(steps) == 1 and steps[0].date == date(2026, 10, 28)
