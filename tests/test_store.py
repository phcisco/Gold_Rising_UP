from __future__ import annotations

from pathlib import Path

import pandas as pd

from goldrising.contracts import IndicatorSeries, Provenance
from goldrising.data.store import CuratedStore


def _prov(as_of: str) -> Provenance:
    return Provenance("treasury", "财政部", "nominal:10 Yr", "https://x", "2026-09-03T00:00:00+00:00", as_of, 1)


def test_roundtrip_and_merge(tmp_path: Path) -> None:
    store = CuratedStore(tmp_path)
    s1 = IndicatorSeries(
        "dgs10", pd.Series([4.0, 4.1], index=pd.to_datetime(["2026-09-01", "2026-09-02"])), _prov("2026-09-02")
    )
    store.save(s1)
    s2 = IndicatorSeries(
        "dgs10", pd.Series([4.15, 4.2], index=pd.to_datetime(["2026-09-02", "2026-09-03"])), _prov("2026-09-03")
    )
    merged = store.save(s2)
    assert list(merged.values) == [4.0, 4.15, 4.2]
    loaded = store.load("dgs10")
    assert loaded is not None
    assert loaded.provenance.as_of == "2026-09-03"
    assert loaded.last_value == 4.2
    assert store.list_ids() == ["dgs10"]
    assert store.load("nope") is None


def test_series_normalizes_index_and_dupes() -> None:
    idx = pd.to_datetime(["2026-09-02 15:00", "2026-09-02 16:00", "2026-09-01 00:00"])
    s = IndicatorSeries("x", pd.Series([1.0, 2.0, 0.5], index=idx), _prov("2026-09-02"))
    assert list(s.values) == [0.5, 2.0]
    assert s.values.index.is_monotonic_increasing
