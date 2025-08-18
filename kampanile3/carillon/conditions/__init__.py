from .condition import Condition
from .minute_condition import MinuteCondition
from .time_condition import TimeCondition


def build_condition(data: dict[str, object]) -> Condition:
    condition_type = data.get("type")
    match condition_type:
        case "time":
            return TimeCondition(data)
        case "minute":
            return MinuteCondition(data)
    raise ValueError(f"Unsupported condition type: {condition_type}")


__all__ = ["Condition", "TimeCondition", "MinuteCondition", "build_condition"]
