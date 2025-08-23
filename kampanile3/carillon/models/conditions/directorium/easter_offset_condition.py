from datetime import date, timedelta

from directorium.utils import easter, normalize_date

from ..comparator_condition import ComparatorCondition


class EasterOffsetCondition(ComparatorCondition):
    """A condition checking if the current date's offset from Easter matches a specified value."""

    @property
    def offset(self) -> int | None:
        try:
            return int(self.data.get("offset"))
        except (TypeError, ValueError):
            return None

    @property
    def left_operand(self) -> date:
        return date.today()

    @property
    def right_operand(self) -> date:
        date = easter(self.left_operand.year) + timedelta(days=self.offset)
        return normalize_date(date)

    def validate(self):
        super().validate()
        if self.offset is None:
            raise ValueError("Invalid offset value")
