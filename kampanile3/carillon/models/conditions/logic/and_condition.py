from django.utils.translation import gettext_lazy as _

from .or_condition import OrCondition


class AndCondition(OrCondition):
    """A condition that checks if all sub-conditions are met."""

    @property
    def is_met(self) -> bool:
        return all(condition.is_met for condition in self.conditions)

    class Meta:
        type = "and"
        label = _("And condition")
        icon = "mdi mdi-ampersand"
        sample_data = {"conditions": []}
        documentation = _("Checks if all sub-conditions are met.")
