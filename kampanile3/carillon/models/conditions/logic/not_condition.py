from ..condition import Condition


class NotCondition(Condition):
    """A condition that negates another condition."""

    @property
    def condition(self) -> Condition:
        from .. import build_condition

        return build_condition(self.data.get("condition"))

    def validate(self):
        self.condition.validate()

    def is_met(self) -> bool:
        return not self.condition.is_met()
