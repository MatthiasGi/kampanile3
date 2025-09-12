from carillon.models import Striker
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Input(models.Model):
    """A model representing a GPIO-input that can trigger a striker."""

    class Behaviour(models.TextChoices):
        """Setting on what input action should call the trigger."""

        DISABLED = "0", _("Disabled")
        ON_INPUT_LOW = "L", _("On input state low")
        ON_INPUT_HIGH = "H", _("On input state high")
        ON_INPUT_CHANGE = "C", _("On change of input state")

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

    striker = models.ForeignKey(
        Striker,
        on_delete=models.CASCADE,
        verbose_name=_("Striker"),
        related_name="+",
    )
    """The striker that should be triggered by this input."""

    behaviour = models.CharField(
        max_length=1,
        choices=Behaviour,
        default=Behaviour.DISABLED,
        verbose_name=_("Behaviour"),
        help_text=_("Which trigger should call the striker?"),
    )
    """The behaviour for triggering this input."""

    def trigger(self):
        """Trigger the striker associated with this input."""
        self.striker.check_rules()

    def get_absolute_url(self):
        return reverse("gpio:inputs:detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Input")
        verbose_name_plural = _("Inputs")
        ordering = ["pin"]
