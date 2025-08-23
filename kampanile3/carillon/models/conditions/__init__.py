from . import date, logic
from .condition import Condition


def build_condition(data: dict[str, object]) -> Condition:
    condition_type = data.get("type")
    match condition_type:
        case "time":
            return date.TimeCondition(data)
        case "minute":
            return date.MinuteCondition(data)
        case "not":
            return logic.NotCondition(data)
        case "and":
            return logic.AndCondition(data)
        case "or":
            return logic.OrCondition(data)
        case _:
            raise ValueError(f"Unsupported condition type: {condition_type}")


__all__ = [
    "Condition",
    "TimeCondition",
    "MinuteCondition",
    "NotCondition",
    "build_condition",
    "AndCondition",
    "OrCondition",
]
