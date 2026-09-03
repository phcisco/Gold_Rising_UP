"""叙事库：叙事卡的加载、结构校验与指标映射。不做任何判断，只检查结构与引用完整性。"""

from goldrising.narratives.cards import (
    CardProblem,
    indicator_narrative_map,
    load_cards,
    validate_card,
    validate_collection,
)

__all__ = ["CardProblem", "indicator_narrative_map", "load_cards", "validate_card", "validate_collection"]
