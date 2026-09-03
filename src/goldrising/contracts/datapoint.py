"""带出处的时间序列。每个数据点都能回答：来自谁、哪个序列、数据截止日、何时抓取、固有滞后。"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class Provenance:
    provider: str
    publisher: str
    series: str
    url: str
    fetched_at: str  # ISO 8601 UTC
    as_of: str  # 最新观测日 ISO date
    lag_days: int
    note: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def now_iso() -> str:
        return datetime.now(UTC).replace(microsecond=0).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Provenance:
        return cls(
            provider=str(d["provider"]),
            publisher=str(d.get("publisher", "")),
            series=str(d.get("series", "")),
            url=str(d.get("url", "")),
            fetched_at=str(d.get("fetched_at", "")),
            as_of=str(d.get("as_of", "")),
            lag_days=int(d.get("lag_days", 0)),
            note=str(d.get("note", "")),
            extra=dict(d.get("extra", {})),
        )


@dataclass
class IndicatorSeries:
    indicator_id: str
    values: pd.Series  # DatetimeIndex（日期，无时区），float 值，升序，无重复
    provenance: Provenance

    def __post_init__(self) -> None:
        s = self.values.dropna().astype(float)
        idx = pd.to_datetime(s.index)
        s.index = pd.DatetimeIndex(idx.tz_localize(None) if idx.tz is not None else idx).normalize()
        s = s[~s.index.duplicated(keep="last")].sort_index()
        s.name = self.indicator_id
        self.values = s

    @property
    def last_date(self) -> date | None:
        if self.values.empty:
            return None
        return self.values.index[-1].date()

    @property
    def last_value(self) -> float | None:
        if self.values.empty:
            return None
        return float(self.values.iloc[-1])

    def merged_with(self, other: IndicatorSeries) -> IndicatorSeries:
        """用 other 的值覆盖同日期旧值，其余并集。出处取 other。"""
        combined = pd.concat([self.values, other.values])
        combined = combined[~combined.index.duplicated(keep="last")].sort_index()
        return IndicatorSeries(self.indicator_id, combined, other.provenance)
