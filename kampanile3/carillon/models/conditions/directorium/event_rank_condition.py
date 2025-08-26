from directorium.event import Rank
from django.utils.translation import gettext_lazy as _

from ..comparator_condition import ComparatorCondition
from .directorium_condition import DirectoriumCondition


class EventRankCondition(DirectoriumCondition, ComparatorCondition):
    """A condition that compares the current liturgical event's rank with a specified rank using a comparator."""

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

    class Meta:
        type = "event_rank"
        label = _("Event rank condition")
        icon = "mdi mdi-calendar-filter-outline"
        sample_data = {"comparator": "eq", "rank": "SOLEMNITY"}
        documentation = _(
            "Compares the current liturgical event's rank with a specified rank using a comparator. Available ranks in ascending importance are: NONE, COMMEMORATION, OPTIONAL_MEMORIAL, MEMORIAL, FEAST, and SOLEMNITY. Available comparators are: gt, gte, lt, lte, eq, and neq."
        )
