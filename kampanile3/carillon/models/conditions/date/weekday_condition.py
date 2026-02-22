from datetime import datetime

from django.utils.translation import gettext_lazy as _

from ..condition import Condition


class WeekdayCondition(Condition):
    """
    A condition that checks if today's weekday matches the specified weekday.
    """

    WEEKDAYS = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    @property
    def weekday(self) -> int | None:
        data = self.data.get("weekday")
        if isinstance(data, str):
            data = data.lower()
            if data in self.WEEKDAYS:
                return self.WEEKDAYS.index(data)
            return None

        try:
            weekday = int(data)
        except (TypeError, ValueError):
            return None
        if 0 <= weekday < 7:
            return weekday

        return None

    def validate(self):
        if self.weekday is None:
            raise ValueError("Invalid weekday")

    @property
    def is_met(self) -> bool:
        return datetime.now().weekday() == self.weekday

    class Meta:
        type = "weekday"
        label = _("Weekday Condition")
        icon = "mdi mdi-calendar-week-begin"
        sample_data = {"weekday": "SUNDAY"}
        documentation = _(
            "A condition that checks if today's weekday matches the specified weekday."
        )
