from django.utils.translation import gettext_lazy as _

from ..condition import Condition


class NotCondition(Condition):
    """A condition that negates another condition."""

    @property
    def condition(self) -> Condition:
        from .. import build_condition

        return build_condition(self.data.get("condition"))

    def validate(self):
        self.condition.validate()

    @property
    def is_met(self) -> bool:
        return not self.condition.is_met

    class Meta:
        type = "not"
        label = _("Not condition")
        icon = "mdi mdi-exclamation"
        sample_data = {"condition": {}}
        documentation = _("A condition that negates another condition.")
