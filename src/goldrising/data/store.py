"""curated 存储：每个指标一个 CSV（date,value）加一个 meta.json（出处）。"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from goldrising.contracts import IndicatorSeries, Provenance


class CuratedStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _csv(self, indicator_id: str) -> Path:
        return self.root / f"{indicator_id}.csv"

    def _meta(self, indicator_id: str) -> Path:
        return self.root / f"{indicator_id}.meta.json"

    def exists(self, indicator_id: str) -> bool:
        return self._csv(indicator_id).exists()

    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob("*.csv"))

    def load(self, indicator_id: str) -> IndicatorSeries | None:
        csv = self._csv(indicator_id)
        if not csv.exists():
            return None
        df = pd.read_csv(csv, parse_dates=["date"])
        values = pd.Series(df["value"].to_numpy(dtype=float), index=pd.DatetimeIndex(df["date"]))
        meta_path = self._meta(indicator_id)
        if meta_path.exists():
            prov = Provenance.from_dict(json.loads(meta_path.read_text(encoding="utf-8")))
        else:
            prov = Provenance(provider="unknown", publisher="", series="", url="", fetched_at="", as_of="", lag_days=0)
        return IndicatorSeries(indicator_id, values, prov)

    def save(self, series: IndicatorSeries, merge: bool = True) -> IndicatorSeries:
        final = series
        if merge:
            existing = self.load(series.indicator_id)
            if existing is not None:
                final = existing.merged_with(series)
        dates = pd.DatetimeIndex(final.values.index).strftime("%Y-%m-%d")
        df = pd.DataFrame({"date": dates, "value": final.values.to_numpy()})
        df.to_csv(self._csv(series.indicator_id), index=False)
        self._meta(series.indicator_id).write_text(
            json.dumps(final.provenance.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return final
