from datetime import date

from directorium.utils import normalize_date

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
