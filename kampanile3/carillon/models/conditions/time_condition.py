from datetime import datetime

from .minute_condition import MinuteCondition


class TimeCondition(MinuteCondition):
    """A condition that comparse the current time with a specific hour and minute."""

    @property
    def hour(self) -> int | None:
        try:
            hour = int(self.data.get("hour"))
        except (TypeError, ValueError):
            return None
        if hour < 0 or hour > 23:
            return None
        return hour

    def validate(self):
        super().validate()
        if self.hour is None:
            raise ValueError("Invalid hour value")
        if self.data.get("comparator") not in ("gt", "gte", "lt", "lte", "eq", "neq"):
            raise ValueError("Invalid comparator value")

    def is_met(self) -> bool:
        now = datetime.now()
        target = datetime(now.year, now.month, now.day, self.hour, self.minute)
        now = datetime(now.year, now.month, now.day, now.hour, now.minute)
        comparator = self.data.get("comparator")
        match comparator:
            case "gt":
                return now > target
            case "gte":
                return now >= target
            case "lt":
                return now < target
            case "lte":
                return now <= target
            case "eq":
                return now == target
            case "neq":
                return now != target
            case _:
                raise ValueError(f"Invalid comparator: {comparator}")
