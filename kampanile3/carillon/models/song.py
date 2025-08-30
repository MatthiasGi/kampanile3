import mido
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Song(models.Model):
    """Model to store a MIDI-file based song."""

    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    """The name of the song for a friendly display."""

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name=_("Slug"),
        help_text=_("Unique identifier for the song to e.g. access it via API."),
    )
    """A unique slug to identify the song or address it e.g. via API."""

    file = models.FileField(upload_to="carillon/songs/", verbose_name=_("MIDI file"))
    """The actual MIDI file containing the song."""

    transpose = models.IntegerField(
        default=0,
        verbose_name=_("Transpose"),
        help_text=_("Transposition in semitones, e.g. -12 for one octave down."),
    )
    """The number of semitones to transpose the song."""

    tempo_multiplier = models.FloatField(
        default=1.0,
        verbose_name=_("Tempo Multiplier"),
        help_text=_(
            "A multiplier for the tempo of the song. This can be used to speed up or slow down the song."
        ),
    )
    """A multiplier for the tempo of the song. This can be used to speed up or slow down the song."""

    @property
    def tempo_percentage(self) -> int:
        """Returns the tempo as a percentage of the original tempo."""
        return int(self.tempo_multiplier * 100)

    @property
    def midiFile(self) -> mido.MidiFile:
        """Simply returns the MIDI-file as a `mido.MidiFile` object."""
        return mido.MidiFile(self.file.path)

    @property
    def fileTempo(self) -> int | None:
        """The tempo read from the file or `None` if not found."""
        for msg in self.midiFile.tracks[0]:
            if msg.type == "set_tempo":
                return msg.tempo
        return None

    def bpm(self) -> float:
        """Returns the BPM (Beats Per Minute) of the song."""
        return mido.tempo2bpm(self.fileTempo)

    @property
    def midi(self) -> list[mido.Message]:
        """A list of MIDI-messages from the file.

        The returned list has already transposed notes and adjusted timing.
        """
        messages: list[mido.Message] = []
        tempo = self.fileTempo / self.tempo_multiplier
        for msg in self.midiFile.tracks[0]:
            if msg.type not in ("note_on", "note_off"):
                continue
            time = mido.tick2second(msg.time, self.midiFile.ticks_per_beat, tempo)
            note = msg.note + self.transpose
            messages.append(msg.copy(time=time, note=note))
        return messages

    def get_absolute_url(self):
        return reverse("carillon:songs:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")
