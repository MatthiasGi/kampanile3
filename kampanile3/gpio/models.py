import board
import digitalio
import microcontroller
from carillon.models import Striker
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

INPUT_PIN_SINGLETON_DATA = {}


class Input(models.Model):
    """A model representing a GPIO-input that can trigger a striker."""

    class Behaviour(models.TextChoices):
        """Setting on what input action should call the trigger."""

        ON_INPUT_LOW = "L", _("On input state low")
        ON_INPUT_HIGH = "H", _("On input state high")
        ON_INPUT_CHANGE = "C", _("On change of input state")

    class Pull(models.TextChoices):
        """Setting for the internal pull resistor of the input pin."""

        NONE = "N", _("No pull resistor")
        UP = "U", _("Pull-up resistor")
        DOWN = "D", _("Pull-down resistor")

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    """The name of the input for a friendly display."""

    pin = models.CharField(
        max_length=10,
        verbose_name=_("I/O-Pin"),
        blank=True,
        default="",
    )
    """The GPIO pin name as provided by the Adafruit Blinka library."""

    active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Whether this input is active and should be monitored."),
    )
    """Whether this input is active and should be monitored."""

    error = models.CharField(
        max_length=255,
        verbose_name=_("Error"),
        blank=True,
        default="",
        help_text=_(
            "An error message if there is an issue with this input. Will be cleared when the input is set active."
        ),
    )
    """An error message if there is an issue with this input."""

    pull = models.CharField(
        max_length=1,
        choices=Pull,
        default=Pull.NONE,
        verbose_name=_("Pull resistor"),
        help_text=_("The internal pull resistor for the input pin."),
    )
    """The internal pull resistor setting for the input pin."""

    striker = models.ForeignKey(
        Striker,
        on_delete=models.CASCADE,
        verbose_name=_("Striker"),
        related_name="+",
        blank=True,
        null=True,
    )
    """The striker that should be triggered by this input."""

    behaviour = models.CharField(
        max_length=1,
        choices=Behaviour,
        default=Behaviour.ON_INPUT_CHANGE,
        verbose_name=_("Behaviour"),
        help_text=_("Which trigger should call the striker?"),
    )
    """The behaviour for triggering this input."""

    def trigger(self):
        """Trigger the striker associated with this input."""
        self.striker.check_rules()

    def get_absolute_url(self):
        return reverse("gpio:inputs:detail", kwargs={"pk": self.pk})

    def deactivate(self, error: str):
        """Deactivate this input with an error message."""
        self.error = error
        self.active = False
        self.save()

    @property
    def board_pin(self):
        if not self.pin or not hasattr(board, self.pin):
            return None
        pin = getattr(board, self.pin)
        if not isinstance(pin, microcontroller.Pin):
            return None
        return pin

    @property
    def pull_setting(self):
        if self.pull == self.Pull.UP:
            return digitalio.Pull.UP
        if self.pull == self.Pull.DOWN:
            return digitalio.Pull.DOWN
        return None

    def save(self, *args, **kwargs):
        if self.active and self.error:
            self.error = ""
        super().save(*args, **kwargs)
        Input.load_pins()

    @staticmethod
    def load_pins():
        inputs = Input.objects.exclude(
            Q(active=False) | Q(pin__isnull=True) | Q(pin__exact="")
        )

        pin_ids = set()
        pins = []

        # Check if all pins exist and are unique
        for input in inputs:
            pin = input.board_pin
            if pin is None:
                input.deactivate(_("The specified pin does not exist on this board."))
                return

            if pin.id in pin_ids:
                input.deactivate(
                    _("The specified pin is already used by another active input.")
                )
                return
            pin_ids.add(pin.id)
            pins.append(pin)

        # Determine pins not longer used anymore
        old_pin_ids = set(INPUT_PIN_SINGLETON_DATA.keys()).difference(pin_ids)
        for id in old_pin_ids:
            INPUT_PIN_SINGLETON_DATA[id].deinit()
            del INPUT_PIN_SINGLETON_DATA[id]

        # Add new pins or update old ones
        for input in inputs:
            pin = input.board_pin
            if pin.id not in INPUT_PIN_SINGLETON_DATA:
                INPUT_PIN_SINGLETON_DATA[pin.id] = digitalio.DigitalInOut(pin)
            INPUT_PIN_SINGLETON_DATA[pin.id].switch_to_input(pull=input.pull_setting)

    class Meta:
        verbose_name = _("Input")
        verbose_name_plural = _("Inputs")
        ordering = ["pin"]
        constraints = [
            UniqueConstraint(
                fields=["pin"],
                condition=Q(active=True) & ~Q(pin=""),
                name="unique_active_pin",
            )
        ]
