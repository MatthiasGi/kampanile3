from django.utils.translation import gettext_lazy as _

from .directorium_condition import DirectoriumCondition


class EventTitleCondition(DirectoriumCondition):
    """A condition checking if the current event title matches a specified value (case-insensitive)."""

    @property
    def title(self) -> str:
        return str(self.data.get("title", "")).strip().lower()

    def validate(self):
        if not self.title:
            raise ValueError("Missing or empty title")

    @property
    def is_met(self) -> bool:
        return self.title == self.directorium.get()[0].title.lower()

    class Meta:
        type = "event_title"
        label = _("Event title condition")
        icon = "mdi mdi-calendar-search-outline"
        sample_data = {"title": ""}
        documentation = _(
            "Checks if the current event title matches a specified value (case-insensitive)."
        )
