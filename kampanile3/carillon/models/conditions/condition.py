from abc import ABC, abstractmethod


class Condition(ABC):
    """The abstract base class for all conditions."""

    def __init__(self, data: dict[str, object]):
        self.data = data

    def is_valid(self) -> bool:
        """Check if the condition is written valid."""
        try:
            self.validate()
            return True
        except ValueError:
            return False

    @abstractmethod
    def validate(self):
        """Validate the data provided to the condition."""
        raise NotImplementedError

    @abstractmethod
    def is_met(self) -> bool:
        """Check if the condition is met."""
        raise NotImplementedError
