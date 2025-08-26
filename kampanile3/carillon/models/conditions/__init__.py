from . import date, directorium, logic
from .condition import Condition

CONDITION_MODULES = (date, logic, directorium)
CONDITION_LOOKUP = {c.meta.type: c for m in CONDITION_MODULES for c in m.CONDITIONS}


def build_condition(data: dict[str, object]) -> Condition:
    condition_type = data.get("type")
    if condition_type in CONDITION_LOOKUP:
        return CONDITION_LOOKUP[condition_type](data)
    raise ValueError(f"Unsupported condition type: {condition_type}")


__all__ = ["Condition", "build_condition", "CONDITION_LOOKUP"]
