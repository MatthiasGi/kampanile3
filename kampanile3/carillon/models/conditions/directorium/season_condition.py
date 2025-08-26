from directorium.directorium import Directorium, Season
from django.utils.translation import gettext_lazy as _

from ..condition import Condition


class SeasonCondition(Condition):
    """Checks if current date is in the given season."""

    @property
    def season(self) -> Season | None:
        try:
            return Season[self.data.get("season", "").upper()]
        except KeyError:
            return None

    def validate(self):
        if self.season is None:
            raise ValueError("Invalid season value")

    @property
    def is_met(self) -> bool:
        return Directorium.get_season() == self.season

    class Meta:
        type = "season"
        label = _("Season condition")
        icon = "mdi mdi-calendar-range-outline"
        sample_data = {"season": "ORDINARY"}
        documentation = _(
            "Checks if the current date is in the specified liturgical season. Available seasons are: ORDINARY, CHRISTMAS, LENT, and EASTER."
        )
