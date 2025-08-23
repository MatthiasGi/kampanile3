from .condition import Condition


class OrCondition(Condition):
    """A condition that checks if at least one of the sub-conditions is met."""

    @property
    def conditions(self) -> list[Condition]:
        from . import build_condition

        return [build_condition(c) for c in self.data.get("conditions", [])]

    def validate(self):
        if not self.conditions:
            raise ValueError("At least one condition must be provided")
        for condition in self.conditions:
            condition.validate()

    def is_met(self) -> bool:
        return any(condition.is_met() for condition in self.conditions)
