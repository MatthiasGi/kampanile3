from abc import abstractmethod

from .condition import Condition


class ComparatorCondition(Condition):
    @property
    def _valid_comparators(self) -> set[str]:
        return {"gt", "gte", "lt", "lte", "eq", "neq"}

    @property
    def comparator(self) -> str | None:
        c = self.data.get("comparator")
        return c if c in self._valid_comparators else None

    def validate(self):
        if self.comparator is None:
            raise ValueError("Invalid comparator value")

    @property
    @abstractmethod
    def left_operand(self) -> any:
        pass

    @property
    @abstractmethod
    def right_operand(self) -> any:
        pass

    def is_met(self) -> bool:
        match self.comparator:
            case "gt":
                return self.left_operand > self.right_operand
            case "gte":
                return self.left_operand >= self.right_operand
            case "lt":
                return self.left_operand < self.right_operand
            case "lte":
                return self.left_operand <= self.right_operand
            case "eq":
                return self.left_operand == self.right_operand
            case "neq":
                return self.left_operand != self.right_operand
            case _:
                raise ValueError(f"Invalid comparator: {self.comparator}")
