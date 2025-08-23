from datetime import datetime

from .minute_modulo_condition import MinuteModuloCondition


class HourModuloCondition(MinuteModuloCondition):
    """A condition that checks the modulo of the current hour."""

    @property
    def remainder(self) -> int | None:
        value = self._valid_int(self.data.get("remainder"))
        if value is None or not (0 <= value < 24):
            return None
        return value

    def is_met(self) -> bool:
        return datetime.now().hour % self.modulo == self.remainder
