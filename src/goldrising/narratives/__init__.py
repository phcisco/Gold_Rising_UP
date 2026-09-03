"""叙事库：叙事卡的加载与结构校验。不做任何判断，只检查结构与引用完整性。"""

from goldrising.narratives.cards import CardProblem, load_cards, validate_card, validate_collection

__all__ = ["CardProblem", "load_cards", "validate_card", "validate_collection"]
