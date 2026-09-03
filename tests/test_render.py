from __future__ import annotations

from goldrising.render.page import fmt_change, fmt_value, render_page
from goldrising.render.svg import percentile_bar, sparkline


def _entry(**over: object) -> dict[str, object]:
    e: dict[str, object] = {
        "id": "dfii10",
        "name": "10 年期 TIPS 实际收益率",
        "group": "opportunity_cost",
        "tier": "1",
        "unit": "pct",
        "decimals": 2,
        "frequency": "daily",
        "lag_days": 1,
        "gold_sign": -1,
        "note": "旧锚",
        "last": 2.45,
        "last_date": "2026-09-02",
        "staleness_days": 1,
        "changes": {
            "1d": {"abs": 0.03, "pct": 1.2},
            "5d": {"abs": 0.1, "pct": 4.0},
            "20d": {"abs": -0.05, "pct": -2.0},
        },
        "pct_1y": 80.0,
        "pct_5y": 90.0,
        "pct_10y": 97.0,
        "pct_all": 97.0,
        "z_250": 1.8,
        "z_change_1d": 0.5,
        "sparkline": [["2026-08-01", 2.3], ["2026-08-15", 2.4], ["2026-09-02", 2.45]],
        "provenance": {
            "provider": "treasury",
            "publisher": "美国财政部",
            "url": "https://home.treasury.gov",
            "fetched_at": "2026-09-03T00:00:00+00:00",
        },
        "flags": [{"code": "extreme_high", "label": "历史高分位", "detail": "分位 97"}],
    }
    e.update(over)
    return e


def test_fmt_helpers() -> None:
    assert fmt_value(2.456, "pct", 2) == "2.46%"
    assert fmt_value(-12.0, "bp", 0) == "-12bp"
    assert fmt_value(4476.6, "usd", 1) == "4,476.6"
    assert fmt_value(None, "usd", 1) == "—"
    txt, cls = fmt_change(_entry(), "1d")
    assert txt == "+3bp" and cls == "up"
    txt2, cls2 = fmt_change(_entry(unit="usd", changes={"1d": {"abs": -10.0, "pct": -0.5}}), "1d")
    assert txt2 == "-0.50%" and cls2 == "down"


def test_svg_helpers() -> None:
    svg = sparkline([["2026-01-01", 1.0], ["2026-01-02", 2.0], ["2026-01-03", 1.5]])
    assert svg.startswith("<svg") and "<path" in svg
    assert "数据不足" in sparkline([["2026-01-01", 1.0]])
    assert "分位 97" in percentile_bar(97.0)
    assert "分位 —" in percentile_bar(None)


def test_render_page_contains_sections() -> None:
    snapshot = {
        "run_date": "2026-09-03",
        "generated_at": "2026-09-03T00:00:00+00:00",
        "groups": [{"id": "opportunity_cost", "name": "机会成本与政策路径", "order": 1, "question": "持有黄金的代价"}],
        "indicators": {
            "dfii10": _entry(),
            "gc_front": _entry(id="gc_front", name="COMEX 黄金", unit="usd", last=4476.6, tier="1", gold_sign=0),
        },
        "missing": ["cb_purchases"],
        "derived_failures": [],
        "fedwatch": {
            "as_of": "2026-09-03",
            "effr": 3.63,
            "method": "复算",
            "meetings": [
                {
                    "date": "2026-09-16",
                    "pre_rate": 3.63,
                    "post_rate": 3.4,
                    "change_bp": -23.0,
                    "cum_change_bp": -23.0,
                    "probabilities": {"-25": 0.92, "0": 0.08},
                    "method": "next_month",
                }
            ],
        },
        "fetch_report": {"results": [{"indicator_id": "hy_oas", "status": "skipped", "message": "缺少 FRED_API_KEY"}]},
    }
    html = render_page(snapshot, archive_dates=["2026-09-02", "2026-09-03"])
    for needle in [
        "今日速览",
        "联邦基金期货隐含路径",
        "L1 行情台",
        "数据来源与口径",
        "10 年期 TIPS 实际收益率",
        "历史高分位",
        "hy_oas",
        "cb_purchases",
        "2026-09-16",
        "不构成投资建议",
    ]:
        assert needle in html
    assert "<script" not in html
