import json
from abc import ABCMeta, abstractmethod


class ConditionMeta(ABCMeta):
    """
    A metaclass for the conditions that enforces the presence of meta data
    inside of a `Meta` class. This ensures, that all conditions have the
    following data:

    - `type`: A unique string identifying the condition type (e.g. `time`). This
      will be used to identify the condition in the JSON-object.
    - `icon`: The class of the icon to be used for the condition (e.g.
      `mdi mdi-clock`).
    - `label`: A human-readable label for the condition.
    - `sample_data`: A dictionary containing sample data for the condition. This
      will be used to generate a sample JSON-object for the condition. The
      required type will be automatically added.
    - `documentation`: A string containing the documentation for the condition
      which can be displayed in the frontend.
    """

    def __init__(cls, name, bases, attrs):
        if getattr(cls, "__abstractmethods__"):
            return
        meta = attrs.get("Meta", None)
        if meta is None:
            raise TypeError("Condition class must have a Meta class")
        attrs = ["icon", "label", "type", "sample_data", "documentation"]
        for attr in attrs:
            if not hasattr(meta, attr):
                raise TypeError(f"Meta class must have a '{attr}' attribute")
        cls.meta = meta
        cls.meta.sample = json.dumps({"type": meta.type, **meta.sample_data})


class Condition(metaclass=ConditionMeta):
    """The abstract base class for all conditions."""

    def __init__(self, data: dict[str, object]):
        self.data = data

    @property
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

    @property
    @abstractmethod
    def is_met(self) -> bool:
        """Check if the condition is met."""
        raise NotImplementedError


class EmptyCondition(Condition):
    """A condition that is always met."""

    class Meta:
        type = None
        icon = None
        label = None
        sample_data = {}
        documentation = "A condition that is always met."

    def validate(self):
        """An empty condition is always valid."""
        pass

    @property
    def is_met(self) -> bool:
        """An empty condition is always met."""
        return True
