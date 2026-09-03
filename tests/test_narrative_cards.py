from __future__ import annotations

from pathlib import Path

import yaml

from goldrising.contracts import load_registry
from goldrising.narratives import load_cards, validate_card, validate_collection

ROOT = Path(__file__).resolve().parents[1]


def _card(**over: object) -> dict[str, object]:
    c: dict[str, object] = {
        "id": "fed_independence",
        "name": "美联储独立性受损",
        "status": "active",
        "lifecycle_state": "边际",
        "lifecycle_since": "2026-09-03",
        "lifecycle_rationale": "理由",
        "pricing_degree": "未定价",
        "pricing_rationale": "理由",
        "direction": "bull",
        "horizon": "3-12m",
        "thesis": "命题",
        "logic_chain": ["a", "b"],
        "regime_dependency": {"passive_fed": "bull", "credible_fed": "bear", "note": "n"},
        "evidence_indicators": [
            {"indicator_id": "t10yie", "expected_sign": "up", "weight": "high", "rationale": "r"},
            {"indicator_id": "curve_2s30s", "expected_sign": "up", "weight": "medium", "rationale": "r"},
        ],
        "verification_signals": [
            {"id": "v1", "description": "d", "type": "qual", "next_check": "2026-09-16"},
            {
                "id": "v2",
                "description": "d",
                "type": "quant",
                "rule": {"indicator_id": "t10yie", "op": "change_gt", "value": 0.15},
                "next_check": "2026-09-30",
            },
            {"id": "v3", "description": "d", "type": "qual", "next_check": "2026-10-01"},
        ],
        "falsification_conditions": [
            {
                "id": "f1",
                "version": 1,
                "created": "2026-09-03",
                "description": "d",
                "type": "quant",
                "rule": {
                    "all_of": [
                        {"indicator_id": "t10yie", "op": "lt", "value": 2.3},
                        {"indicator_id": "curve_2s30s", "op": "lt", "value": 0.8},
                    ]
                },
                "deadline": "2026-11-30",
            }
        ],
        "tensions": [{"narrative_id": "credible_fed_regime", "note": "n"}],
        "news_queries": ["a", "b", "c"],
        "counterargument": "c",
        "sources": [
            {"title": "t", "url": "https://x", "publisher": "p", "accessed": "2026-09-03", "type": "primary"},
            {"title": "t", "url": "https://x", "publisher": "p", "accessed": "2026-09-03", "type": "primary"},
            {"title": "t", "url": "https://x", "publisher": "p", "accessed": "2026-09-03", "type": "primary"},
        ],
        "history": [],
    }
    c.update(over)
    return c


def test_valid_card_has_no_errors() -> None:
    reg = load_registry(ROOT / "indicators" / "registry.yaml")
    problems = validate_card(_card(), reg)
    assert [p for p in problems if p.level == "error"] == []


def test_unknown_indicator_and_bad_enums_are_errors() -> None:
    reg = load_registry(ROOT / "indicators" / "registry.yaml")
    bad = _card(
        lifecycle_state="随便",
        evidence_indicators=[{"indicator_id": "nope", "expected_sign": "sideways", "weight": "high"}],
    )
    msgs = [p.message for p in validate_card(bad, reg) if p.level == "error"]
    assert any("lifecycle_state" in m for m in msgs)
    assert any("nope" in m for m in msgs)
    assert any("expected_sign" in m for m in msgs)


def test_proposed_indicator_is_accepted() -> None:
    reg = load_registry(ROOT / "indicators" / "registry.yaml")
    card = _card(
        proposed_indicators=[{"id": "term_premium_10y", "name": "n", "source": "NY Fed", "frequency": "daily"}],
        evidence_indicators=[
            {"indicator_id": "term_premium_10y", "expected_sign": "up", "weight": "high", "rationale": "r"},
            {"indicator_id": "dxy", "expected_sign": "down", "weight": "low", "rationale": "r"},
        ],
    )
    assert [p for p in validate_card(card, reg) if p.level == "error"] == []


def test_missing_falsification_is_error() -> None:
    problems = validate_card(_card(falsification_conditions=[]))
    assert any("证伪" in p.message for p in problems if p.level == "error")


def test_collection_detects_duplicates_and_dangling_tensions(tmp_path: Path) -> None:
    (tmp_path / "a.yaml").write_text(yaml.safe_dump(_card(id="a"), allow_unicode=True), encoding="utf-8")
    (tmp_path / "b.yaml").write_text(yaml.safe_dump(_card(id="a"), allow_unicode=True), encoding="utf-8")
    (tmp_path / "broken.yaml").write_text("id: [unclosed", encoding="utf-8")
    cards = load_cards(tmp_path)
    problems = validate_collection(cards)
    msgs = [p.message for p in problems]
    assert any("重复" in m for m in msgs)
    assert any("不一致" in m for m in msgs)  # 文件名 b.yaml 与 id a
    assert any("解析失败" in m for m in msgs)
    assert any("credible_fed_regime" in m for m in msgs)


def test_load_cards_skips_drafts_and_meta(tmp_path: Path) -> None:
    (tmp_path / "a.yaml").write_text(yaml.safe_dump(_card(id="a"), allow_unicode=True), encoding="utf-8")
    (tmp_path / "_library.yaml").write_text("version: 1\n", encoding="utf-8")
    (tmp_path / "drafts" / "c1").mkdir(parents=True)
    (tmp_path / "drafts" / "c1" / "b.yaml").write_text(
        yaml.safe_dump(_card(id="b"), allow_unicode=True), encoding="utf-8"
    )
    assert [p.name for p in load_cards(tmp_path)] == ["a.yaml"]
    assert len(load_cards(tmp_path, include_drafts=True)) == 2


def test_indicator_narrative_map_excludes_archived() -> None:
    from goldrising.narratives import indicator_narrative_map

    cards = {Path("a.yaml"): _card(id="a"), Path("b.yaml"): _card(id="b", status="archived", lifecycle_state="归档")}
    m = indicator_narrative_map(cards)
    assert [x["narrative_id"] for x in m["t10yie"]] == ["a"]
