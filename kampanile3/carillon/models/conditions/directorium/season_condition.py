from directorium.directorium import Directorium, Season

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

    def is_met(self) -> bool:
        return Directorium.get_season() == self.season
