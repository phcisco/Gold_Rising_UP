"""联邦基金期货隐含路径的纯函数实现（CME FedWatch 公开方法）。"""

from __future__ import annotations

import calendar
import math
from dataclasses import asdict, dataclass
from datetime import date

STEP_BP = 25.0


@dataclass(frozen=True)
class MeetingStep:
    date: date
    pre_rate: float
    post_rate: float
    change_bp: float
    cum_change_bp: float
    probabilities: dict[str, float]  # 例如 {"-25": 0.7, "0": 0.3}
    method: str  # next_month | intra_month

    def to_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["date"] = self.date.isoformat()
        return d


def step_probabilities(change_bp: float) -> dict[str, float]:
    """把期望变动拆成相邻两档 25bp 结果的概率（CME 二结果假设）。"""
    x = change_bp / STEP_BP
    lower = math.floor(x + 1e-9)
    upper = lower + 1
    p_upper = x - lower
    if p_upper < 1e-9:
        return {_label(lower * STEP_BP): 1.0}
    return {_label(lower * STEP_BP): round(1 - p_upper, 4), _label(upper * STEP_BP): round(p_upper, 4)}


def _label(bp: float) -> str:
    v = round(bp)
    return f"{v:+d}" if v != 0 else "0"


def _next_month(y: int, m: int) -> tuple[int, int]:
    return (y + 1, 1) if m == 12 else (y, m + 1)


def compute_path(
    asof: date,
    contract_rates: dict[tuple[int, int], float],
    effr: float,
    meetings: list[date],
) -> list[MeetingStep]:
    """
    contract_rates: {(年, 月): 合约隐含月均利率（100 - 价格）}
    返回 asof 之后、有合约覆盖的每次会议的会前/会后利率与概率。
    """
    upcoming = [d for d in sorted(meetings) if d > asof]
    meeting_months = {(d.year, d.month) for d in upcoming}
    steps: list[MeetingStep] = []
    pre = effr
    for d in upcoming:
        ym = (d.year, d.month)
        if ym not in contract_rates:
            break
        avg = contract_rates[ym]
        n_days = calendar.monthrange(d.year, d.month)[1]
        days_before = d.day  # 决议日当天仍按会前利率
        days_after = n_days - days_before
        nxt = _next_month(*ym)
        if nxt in contract_rates and nxt not in meeting_months:
            post = contract_rates[nxt]
            method = "next_month"
        elif days_after > 0:
            post = (avg * n_days - pre * days_before) / days_after
            method = "intra_month"
        else:
            break
        change = (post - pre) * 100.0
        steps.append(
            MeetingStep(
                date=d,
                pre_rate=round(pre, 4),
                post_rate=round(post, 4),
                change_bp=round(change, 2),
                cum_change_bp=round((post - effr) * 100.0, 2),
                probabilities=step_probabilities(change),
                method=method,
            )
        )
        pre = post
    return steps
