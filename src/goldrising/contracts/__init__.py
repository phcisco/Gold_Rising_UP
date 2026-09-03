"""数据契约：指标注册表、数据点与出处。contracts 不依赖任何下游模块。"""

from goldrising.contracts.datapoint import IndicatorSeries, Provenance
from goldrising.contracts.registry import (
    Derived,
    GroupMeta,
    Indicator,
    Registry,
    RegistryError,
    Source,
    load_registry,
)

__all__ = [
    "Derived",
    "GroupMeta",
    "Indicator",
    "IndicatorSeries",
    "Provenance",
    "Registry",
    "RegistryError",
    "Source",
    "load_registry",
]
