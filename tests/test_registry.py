from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from goldrising.contracts import RegistryError, load_registry


def test_seed_registry_is_valid(registry_path: Path) -> None:
    reg = load_registry(registry_path)
    assert len(reg.indicators) > 40
    assert reg.by_id("dfii10").tier == "1"
    assert reg.by_id("t10yie").is_derived
    order = [i.id for i in reg.derived_in_order()]
    # 派生指标的输入必须排在它前面（或是基础指标）
    pos = {iid: n for n, iid in enumerate(order)}
    for ind in reg.derived_in_order():
        assert ind.derived is not None
        for dep in ind.derived.inputs:
            if dep in pos:
                assert pos[dep] < pos[ind.id]


def test_every_indicator_has_group_and_tier(registry_path: Path) -> None:
    reg = load_registry(registry_path)
    group_ids = {g.id for g in reg.groups}
    for ind in reg.indicators:
        assert ind.group in group_ids
        assert ind.tier in {"1", "2", "3", "target"}
        assert ind.source.publisher or ind.is_derived


def _write(tmp_path: Path, data: dict[str, object]) -> Path:
    p = tmp_path / "registry.yaml"
    p.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    return p


def _base(**overrides: object) -> dict[str, object]:
    ind: dict[str, object] = {
        "id": "a",
        "name": "甲",
        "group": "g",
        "tier": "1",
        "unit": "pct",
        "frequency": "daily",
        "gold_sign": 1,
        "source": {"provider": "treasury", "series": "nominal:10 Yr", "publisher": "x"},
    }
    ind.update(overrides)
    return ind


def test_duplicate_ids_rejected(tmp_path: Path) -> None:
    p = _write(tmp_path, {"version": 1, "groups": [{"id": "g", "name": "组"}], "indicators": [_base(), _base()]})
    with pytest.raises(RegistryError, match="重复"):
        load_registry(p)


def test_unknown_provider_rejected(tmp_path: Path) -> None:
    bad = _base(source={"provider": "bloomberg", "publisher": "x"})
    p = _write(tmp_path, {"version": 1, "groups": [{"id": "g", "name": "组"}], "indicators": [bad]})
    with pytest.raises(RegistryError, match="未知数据提供方"):
        load_registry(p)


def test_derived_missing_input_rejected(tmp_path: Path) -> None:
    d = _base(id="d", source={"provider": "derived"}, derived={"op": "sub", "inputs": ["a", "zzz"]})
    p = _write(tmp_path, {"version": 1, "groups": [{"id": "g", "name": "组"}], "indicators": [_base(), d]})
    with pytest.raises(RegistryError, match="不存在"):
        load_registry(p)


def test_derived_cycle_rejected(tmp_path: Path) -> None:
    d1 = _base(id="d1", source={"provider": "derived"}, derived={"op": "sub", "inputs": ["d2", "a"]})
    d2 = _base(id="d2", source={"provider": "derived"}, derived={"op": "sub", "inputs": ["d1", "a"]})
    p = _write(tmp_path, {"version": 1, "groups": [{"id": "g", "name": "组"}], "indicators": [_base(), d1, d2]})
    with pytest.raises(RegistryError, match="循环"):
        load_registry(p)
