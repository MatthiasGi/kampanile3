import time

import mido
import mido.backends.rtmidi
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

CARILLON_PORTS = {}


class Carillon(models.Model):
    """A model that does the actual playing of MIDI files."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    """The name of the carillon for a friendly display."""

    port_name = models.CharField(
        max_length=255,
        verbose_name=_("Port Name"),
        help_text=_("The name of the serial port used to connect to the carillon."),
        blank=True,
        default="",
    )
    """The name of the serial port that should be used for the output."""

    @property
    def port(self) -> mido.backends.rtmidi.Output:
        """Get the MIDI port for this carillon."""
        if self.pk not in CARILLON_PORTS or CARILLON_PORTS[self.pk].closed:
            CARILLON_PORTS[self.pk] = mido.open_output(
                self.port_name if self.port_name else None
            )
        return CARILLON_PORTS[self.pk]

    def hit(self, note: int):
        """Hit a note on the carillon."""
        self.port.send(mido.Message("note_on", note=note))
        self.port.send(mido.Message("note_off", note=note))

    def play(self, messages: list[mido.Message]):
        """Play a list of MIDI messages on the carillon."""
        for msg in messages:
            time.sleep(msg.time)
            if msg.type == "note_on" and msg.velocity != 0:
                self.hit(msg.note)

    def get_absolute_url(self):
        return reverse("carillon:carillons:detail", kwargs={"pk": self.pk})
