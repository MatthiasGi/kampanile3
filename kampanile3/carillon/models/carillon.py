import time
from dataclasses import dataclass
from threading import Thread

import mido
import mido.backends.rtmidi
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..signals import carillon_play, carillon_stop

CARILLON_SINGLETON_DATA = {}


class Carillon(models.Model):
    """A model that does the actual playing of MIDI files."""

    @dataclass
    class SingletonData:
        """Object to hold singleton data that should be unique for carillons."""

        port: mido.backends.rtmidi.Output | None = None
        """The MIDI output port for this carillon."""

        thread: Thread | None = None
        """The thread that is currently playing a song on this carillon."""

        priority: int = 0
        """The priority of the current song being played on this carillon."""

        stopped: bool = False
        """Whether the current song has been stopped."""

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

    default = models.BooleanField(
        default=False,
        verbose_name=_("Default"),
        help_text=_(
            "Whether this carillon is the default carillon. Only one carillon can be the default. If activated here, another carillon that was the default will loose that status."
        ),
    )
    """Whether this carillon is the default carillon."""

    active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_(
            "Whether this carillon is active and can be used. May be deactivated to mute all songs."
        ),
    )
    """Whether this carillon is active and can be used. If it is not active, no songs will be played."""

    @property
    def _singleton_data(self) -> SingletonData:
        """Get the singleton data for this carillon."""
        if self.pk not in CARILLON_SINGLETON_DATA:
            CARILLON_SINGLETON_DATA[self.pk] = Carillon.SingletonData()
        return CARILLON_SINGLETON_DATA[self.pk]

    @property
    def port(self) -> mido.backends.rtmidi.Output:
        """Get the MIDI port for this carillon."""
        if not self._singleton_data.port or self._singleton_data.port.closed:
            self._singleton_data.port = mido.open_output(
                self.port_name if self.port_name else None
            )
        return self._singleton_data.port

    @staticmethod
    def get_default() -> "Carillon":
        """Get the default carillon."""
        return Carillon.objects.filter(default=True).first()

    def hit(self, note: int):
        """Hit a note on the carillon."""
        self.port.send(mido.Message("note_on", note=note))
        self.port.send(mido.Message("note_off", note=note))

    def play(self, messages: list[mido.Message], priority: int = 0) -> bool:
        """
        Play a list of MIDI messages on the carillon. If a song is already
        playing, it will be aborted if the priority is equal or higher than the
        current song's priority. Returns if the song was started or not.
        """
        if not self.active:
            return False
        data = self._singleton_data
        if data.thread and data.thread.is_alive():
            if data.priority >= priority:
                return False
            self.stop()

        self.port  # Trying to open the port to ensure it is ready for use.
        data.priority = priority
        data.thread = Thread(target=self._threaded_play, args=(messages,))
        data.thread.start()
        carillon_play.send(sender=self.__class__, carillon=self, priority=priority)
        return True

    def set_volume(self, volume: int):
        """Sends a MIDI-message to set the volume of the carillon."""
        volume = max(0, min(127, volume))  # Clamp the volume to 0-127
        self.port.send(mido.Message("control_change", control=7, value=volume))

    def _threaded_play(self, messages: list[mido.Message]):
        """Internal method to play MIDI messages in a separate thread."""
        for msg in messages:
            if self._singleton_data.stopped:
                return
            time.sleep(msg.time)
            if self._singleton_data.stopped:
                return
            if msg.type == "note_on" and msg.velocity != 0:
                self.hit(msg.note)
        carillon_stop.send(sender=self.__class__, carillon=self)

    def stop(self):
        """Stop the current song playing on the carillon."""
        data = self._singleton_data
        if not data.thread or not data.thread.is_alive():
            return
        data.stopped = True
        data.thread.join()
        data.stopped = False
        data.port.reset()
        carillon_stop.send(sender=self.__class__, carillon=self)

    def save(self, *args, **kwargs):
        """Override save to ensure only one carillon is default."""
        if self.default:
            Carillon.objects.filter(default=True).update(default=False)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("carillon:carillons:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Carillon")
        verbose_name_plural = _("Carillons")
