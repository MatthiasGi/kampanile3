from . import date, directorium, logic
from .condition import Condition

__all__ = ["Condition", "build_condition"]


def build_condition(data: dict[str, object]) -> Condition:
    condition_type = data.get("type")
    for c in (date, logic, directorium):
        if condition_type in c.CONDITIONS:
            return c.CONDITIONS[condition_type](data)
    raise ValueError(f"Unsupported condition type: {condition_type}")
