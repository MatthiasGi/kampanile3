from datetime import datetime

from django.utils.translation import gettext_lazy as _

from ..comparator_condition import ComparatorCondition


class TimeCondition(ComparatorCondition):
    """A condition that comparse the current time with a specific hour and minute."""

    @property
    def minute(self) -> int | None:
        try:
            minute = int(self.data.get("minute"))
        except (TypeError, ValueError):
            return None
        if minute < 0 or minute > 59:
            return None
        return minute

    @property
    def hour(self) -> int | None:
        try:
            hour = int(self.data.get("hour"))
        except (TypeError, ValueError):
            return None
        if hour < 0 or hour > 23:
            return None
        return hour

    @property
    def left_operand(self) -> datetime:
        now = datetime.now()
        return datetime(now.year, now.month, now.day, now.hour, now.minute)

    @property
    def right_operand(self) -> datetime:
        now = datetime.now()
        return datetime(now.year, now.month, now.day, self.hour, self.minute)

    def validate(self):
        super().validate()
        if self.minute is None:
            raise ValueError("Invalid minute value")
        if self.hour is None:
            raise ValueError("Invalid hour value")

    class Meta:
        type = "time"
        label = _("Time condition")
        icon = "mdi mdi-clock"
        sample_data = {"comparator": "eq", "hour": 0, "minute": 0}
        documentation = _(
            "Compares the current time with a specified hour and minute. Available comparators are: gt, gte, lt, lte, eq, and neq."
        )
