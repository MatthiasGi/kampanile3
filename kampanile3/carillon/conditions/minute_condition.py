from datetime import datetime

from .condition import Condition


class MinuteCondition(Condition):
    """A condition checking if the current minute matches a specified value."""

    @property
    def minute(self) -> int | None:
        try:
            minute = int(self.data.get("minute"))
        except (TypeError, ValueError):
            return None
        if minute < 0 or minute > 59:
            return None
        return minute

    def validate(self):
        if self.minute is None:
            raise ValueError("Invalid minute value")

    def is_met(self) -> bool:
        return datetime.now().minute == self.minute
