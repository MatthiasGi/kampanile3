from .and_condition import AndCondition
from .not_condition import NotCondition
from .or_condition import OrCondition

CONDITIONS = {
    "and": AndCondition,
    "or": OrCondition,
    "not": NotCondition,
}

__all__ = [c.__name__ for c in CONDITIONS.values()]
