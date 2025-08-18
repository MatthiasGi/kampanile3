from .and_condition import AndCondition
from .condition import Condition
from .minute_condition import MinuteCondition
from .not_condition import NotCondition
from .or_condition import OrCondition
from .time_condition import TimeCondition


def build_condition(data: dict[str, object]) -> Condition:
    condition_type = data.get("type")
    match condition_type:
        case "time":
            return TimeCondition(data)
        case "minute":
            return MinuteCondition(data)
        case "not":
            return NotCondition(data)
        case "and":
            return AndCondition(data)
        case "or":
            return OrCondition(data)
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
