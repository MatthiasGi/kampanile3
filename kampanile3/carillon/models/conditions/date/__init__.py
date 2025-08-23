from .hour_modulo_condition import HourModuloCondition
from .minute_condition import MinuteCondition
from .minute_modulo_condition import MinuteModuloCondition
from .time_condition import TimeCondition

CONDITIONS = {
    "time": TimeCondition,
    "minute": MinuteCondition,
    "minute_modulo": MinuteModuloCondition,
    "hour_modulo": HourModuloCondition,
}

__all__ = [c.__name__ for c in CONDITIONS.values()]
