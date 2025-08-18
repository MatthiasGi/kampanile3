from .or_condition import OrCondition


class AndCondition(OrCondition):
    """A condition that checks if all sub-conditions are met."""

    def is_met(self) -> bool:
        return all(condition.is_met() for condition in self.conditions)
