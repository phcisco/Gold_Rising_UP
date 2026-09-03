"""派生指标运算。输入为已入库的基础序列，输出新序列；不访问网络。"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd

from goldrising.contracts import Indicator


def _align(inputs: Mapping[str, pd.Series], ids: tuple[str, ...], ffill_limit: int = 5) -> pd.DataFrame:
    frames = {iid: inputs[iid] for iid in ids}
    df = pd.concat(frames, axis=1).sort_index()
    return df.ffill(limit=ffill_limit).dropna()


def compute_derived(indicator: Indicator, inputs: Mapping[str, pd.Series]) -> pd.Series:
    assert indicator.derived is not None
    op = indicator.derived.op
    ids = indicator.derived.inputs
    params = indicator.derived.params
    missing = [i for i in ids if i not in inputs]
    if missing:
        raise KeyError(f"{indicator.id}: 缺少输入 {missing}")

    if op in {"sub", "div", "mul"}:
        df = _align(inputs, ids)
        a, b = df[ids[0]], df[ids[1]]
        if op == "sub":
            out = a - b
        elif op == "div":
            out = a / b.replace(0, np.nan)
        else:
            out = a * b
        return out.dropna()

    s = inputs[ids[0]].dropna()
    window = int(params.get("window", 20))
    if op == "pct_rank":
        min_periods = max(20, window // 4)

        def _rank(w: np.ndarray) -> float:
            last = w[-1]
            return float(100.0 * (np.sum(w < last) + 0.5 * np.sum(w == last)) / w.shape[0])

        return s.rolling(window, min_periods=min_periods).apply(_rank, raw=True).dropna()
    if op == "ma_dist":
        ma = s.rolling(window, min_periods=window).mean()
        return ((s / ma - 1.0) * 100.0).dropna()
    if op == "mom":
        return ((s / s.shift(window) - 1.0) * 100.0).dropna()
    if op == "beta":
        df = _align(inputs, ids)
        ra = df[ids[0]].pct_change()
        rb = df[ids[1]].pct_change()
        cov = ra.rolling(window, min_periods=window).cov(rb)
        var = rb.rolling(window, min_periods=window).var()
        return (cov / var.replace(0, np.nan)).dropna()
    if op == "lev_decay":
        lev = float(params.get("leverage", 3))
        df = _align(inputs, ids)
        a = df[ids[0]]
        b = df[ids[1]]
        ret_a = (a / a.shift(window) - 1.0) * 100.0
        ret_b = (b / b.shift(window) - 1.0) * 100.0
        return (ret_a - lev * ret_b).dropna()
    if op == "ratio_pct_change_diff":
        df = _align(inputs, ids)
        a = df[ids[0]].pct_change(window) * 100.0
        b = df[ids[1]].pct_change(window) * 100.0
        return (a - b).dropna()
    raise ValueError(f"{indicator.id}: 未知派生运算 {op}")
