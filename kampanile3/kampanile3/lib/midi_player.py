import time

import mido
import mido.backends.rtmidi


class MIDIPlayer:
    """A class that outputs MIDI messages."""

    def __init__(self, port: mido.backends.rtmidi.Output = None):
        self.port = mido.open_output() if port is None else port

    def hit(self, note: int):
        self.port.send(mido.Message("note_on", note=note))
        self.port.send(mido.Message("note_off", note=note))

    def play(self, messages: list[mido.Message]):
        for msg in messages:
            time.sleep(msg.time)
            if msg.type == "note_on" and msg.velocity != 0:
                self.hit(msg.note)
