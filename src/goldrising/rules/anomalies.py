"""指标级异动标记。阈值明确、可测试、不含综合判断。"""

from __future__ import annotations

from typing import Any

Z_CHANGE_THRESHOLD = 2.5
PCTL_EXTREME_HIGH = 95.0
PCTL_EXTREME_LOW = 5.0
STALE_GRACE_DAYS = 4


def flag_indicator(entry: dict[str, Any], frequency: str, lag_days: int) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    z1 = entry.get("z_change_1d")
    if isinstance(z1, int | float) and abs(z1) >= Z_CHANGE_THRESHOLD:
        direction = "上行" if z1 > 0 else "下行"
        flags.append({"code": "jump", "label": f"单日异动{direction}", "detail": f"日变动 z 分 {z1:+.1f}"})
    pctl = entry.get("pct_10y")
    if pctl is None:
        pctl = entry.get("pct_5y")
    if isinstance(pctl, int | float):
        if pctl >= PCTL_EXTREME_HIGH:
            flags.append({"code": "extreme_high", "label": "历史高分位", "detail": f"分位 {pctl:.0f}"})
        elif pctl <= PCTL_EXTREME_LOW:
            flags.append({"code": "extreme_low", "label": "历史低分位", "detail": f"分位 {pctl:.0f}"})
    stale = entry.get("staleness_days")
    allowance = {
        "daily": lag_days + STALE_GRACE_DAYS,
        "weekly": lag_days + 10,
        "monthly": lag_days + 40,
        "quarterly": lag_days + 100,
    }
    if isinstance(stale, int) and stale > allowance.get(frequency, lag_days + STALE_GRACE_DAYS):
        flags.append({"code": "stale", "label": "数据陈旧", "detail": f"距最新观测 {stale} 天"})
    return flags
