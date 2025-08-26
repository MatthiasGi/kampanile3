from datetime import datetime

from django.utils.translation import gettext_lazy as _

from .minute_modulo_condition import MinuteModuloCondition


class HourModuloCondition(MinuteModuloCondition):
    """A condition that checks the modulo of the current hour."""

    @property
    def remainder(self) -> int | None:
        value = self._valid_int(self.data.get("remainder"))
        if value is None or not (0 <= value < 24):
            return None
        return value

    @property
    def is_met(self) -> bool:
        return datetime.now().hour % self.modulo == self.remainder

    class Meta:
        type = "hour_modulo"
        label = _("Hour modulo condition")
        icon = "mdi mdi-alarm"
        sample_data = {"modulo": 2, "remainder": 0}
        documentation = _(
            "Checks if the current hour divided by the specified modulo has the specified remainder."
        )
