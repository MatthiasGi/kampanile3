from datetime import datetime

from ..condition import Condition


class MinuteModuloCondition(Condition):
    """A condition that checks the modulo of the current miunte."""

    def _valid_int(self, value) -> int | None:
        try:
            value = int(value)
        except (TypeError, ValueError):
            return None
        return value

    @property
    def modulo(self) -> int | None:
        value = self._valid_int(self.data.get("modulo"))
        if value is None or value <= 0:
            return None
        return value

    @property
    def remainder(self) -> int | None:
        value = self._valid_int(self.data.get("remainder"))
        if value is None or not (0 <= value < 60):
            return None
        return value

    def validate(self):
        if self.modulo is None:
            raise ValueError("Invalid modulo value")
        if self.remainder is None:
            raise ValueError("Invalid remainder value")

    def is_met(self) -> bool:
        return datetime.now().minute % self.modulo == self.remainder
