"""单序列统计量：分位、z 分、多期变动、陈旧度。"""

from __future__ import annotations

import math
from datetime import date

import numpy as np
import pandas as pd

HORIZONS: dict[str, int] = {"1d": 1, "5d": 5, "20d": 20, "60d": 60, "250d": 250}
WEEKLY_HORIZONS: dict[str, int] = {"1d": 1, "5d": 1, "20d": 4, "60d": 13, "250d": 52}


def _clean(v: float) -> float | None:
    return None if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))) else float(v)


def percentile_of_last(values: pd.Series, window: int | None = None, min_obs: int = 30) -> float | None:
    s = values.dropna()
    if window is not None:
        s = s.iloc[-window:]
    if s.shape[0] < min_obs:
        return None
    last = float(s.iloc[-1])
    arr = s.to_numpy(dtype=float)
    below = np.sum(arr < last)
    equal = np.sum(arr == last)
    return _clean(100.0 * (below + 0.5 * equal) / arr.shape[0])


def zscore_of_last(values: pd.Series, window: int = 250, min_obs: int = 30) -> float | None:
    s = values.dropna().iloc[-window:]
    if s.shape[0] < min_obs:
        return None
    sd = float(s.std(ddof=1))
    if sd == 0 or math.isnan(sd):
        return None
    return _clean((float(s.iloc[-1]) - float(s.mean())) / sd)


def zscore_of_last_change(values: pd.Series, window: int = 250, min_obs: int = 30) -> float | None:
    diffs = values.dropna().diff().dropna().iloc[-window:]
    if diffs.shape[0] < min_obs:
        return None
    sd = float(diffs.std(ddof=1))
    if sd == 0 or math.isnan(sd):
        return None
    return _clean((float(diffs.iloc[-1]) - float(diffs.mean())) / sd)


def changes(values: pd.Series, weekly: bool = False) -> dict[str, dict[str, float | None]]:
    s = values.dropna()
    out: dict[str, dict[str, float | None]] = {}
    horizons = WEEKLY_HORIZONS if weekly else HORIZONS
    last = float(s.iloc[-1]) if not s.empty else None
    for label, n in horizons.items():
        if last is None or s.shape[0] <= n:
            out[label] = {"abs": None, "pct": None}
            continue
        prev = float(s.iloc[-1 - n])
        abs_chg = last - prev
        pct = (last / prev - 1.0) * 100.0 if prev != 0 else None
        out[label] = {"abs": _clean(abs_chg), "pct": _clean(pct) if pct is not None else None}
    return out


def staleness_days(last_date: date | None, today: date) -> int | None:
    if last_date is None:
        return None
    return (today - last_date).days


def sparkline_points(values: pd.Series, n: int = 120) -> list[list[object]]:
    s = values.dropna().iloc[-n:]
    dates = pd.DatetimeIndex(s.index).strftime("%Y-%m-%d")
    return [[d, round(float(v), 6)] for d, v in zip(dates, s.to_numpy(dtype=float), strict=True)]
