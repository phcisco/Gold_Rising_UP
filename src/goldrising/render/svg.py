"""内联 SVG：迷你趋势线与分位条。纯函数，确定性输出。"""

from __future__ import annotations

from collections.abc import Sequence


def sparkline(
    points: Sequence[Sequence[object]], width: int = 240, height: int = 46, color: str = "var(--paper)"
) -> str:
    vals = [float(p[1]) for p in points if p and isinstance(p[1], int | float)]
    if len(vals) < 2:
        return f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="数据不足"></svg>'
    lo, hi = min(vals), max(vals)
    span = hi - lo if hi != lo else 1.0
    pad = 3
    n = len(vals)
    xs = [pad + (width - 2 * pad) * i / (n - 1) for i in range(n)]
    ys = [pad + (height - 2 * pad) * (1 - (v - lo) / span) for v in vals]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(zip(xs, ys, strict=True)))
    last_x, last_y = xs[-1], ys[-1]
    first_label = str(points[0][0])[:10]
    last_label = str(points[-1][0])[:10]
    return (
        f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img" '
        f'aria-label="{first_label} 至 {last_label} 走势">'
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.6" vector-effect="non-scaling-stroke"/>'
        f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="2.4" fill="var(--metal)"/>'
        "</svg>"
    )


def percentile_bar(pct: float | None, label: str = "") -> str:
    if pct is None:
        return '<div class="pbar"><span class="lbl">分位 —</span></div>'
    p = max(0.0, min(100.0, pct))
    return (
        f'<div class="pbar"><i style="left:calc({p:.1f}% - 1px)"></i><span class="lbl">{label}分位 {p:.0f}</span></div>'
    )
