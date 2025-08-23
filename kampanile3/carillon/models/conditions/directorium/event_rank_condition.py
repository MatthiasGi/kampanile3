from directorium.event import Rank

from ..comparator_condition import ComparatorCondition
from .directorium_condition import DirectoriumCondition


class EventRankCondition(DirectoriumCondition, ComparatorCondition):
    """A condition that compares the current liturgical event's rank with a specified rank using a comparator."""

    @property
    def comparator(self) -> str | None:
        if self.data.get("comparator") is None:
            return "eq"
        return super().comparator

    @property
    def rank(self) -> Rank | None:
        try:
            return Rank[self.data.get("rank", "").upper()]
        except KeyError:
            return None

    def validate(self):
        super().validate()
        if self.rank is None:
            raise ValueError("Invalid rank value")

    @property
    def left_operand(self) -> Rank:
        return self.directorium.get()[0].rank

    @property
    def right_operand(self) -> Rank:
        return self.rank
