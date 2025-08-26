from datetime import date

from directorium.utils import normalize_date
from django.utils.translation import gettext_lazy as _

from ..comparator_condition import ComparatorCondition


class DateCondition(ComparatorCondition):
    """A condition that compares the current date with a specified date using a comparator."""

    @property
    def date(self) -> str | None:
        try:
            return normalize_date(
                date.today().year, self.data.get("month"), self.data.get("day")
            )
        except (TypeError, ValueError):
            return None

    def validate(self):
        super().validate()
        if self.date is None:
            raise ValueError("Invalid date value")

    @property
    def left_operand(self) -> date:
        return date.today()

    @property
    def right_operand(self) -> date:
        return self.date

    class Meta:
        type = "date"
        label = _("Date condition")
        icon = "mdi mdi-calendar"
        sample_data = {"comparator": "eq", "day": 1, "month": 1}
        documentation = _(
            "Compares the current date with a specified date. Available comparators are: gt, gte, lt, lte, eq, and neq."
        )
