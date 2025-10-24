"""Adding functionality to play selected songs via MQTT"""

from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import (
    Button,
    ButtonInfo,
    Number,
    NumberInfo,
    Select,
    SelectInfo,
)
from paho.mqtt.client import Client, MQTTMessage

from .module import Module


class Jukebox(Module):
    def init_sensors(self):
        self._selected_song = None
        self._priority = 0
        self._tempo = 1.0

        self._init_song_select()
        self._init_play_button()
        self._init_stop_button()
        self._init_priority_number()

        def update_song_list(**kwargs):
            from carillon.models import Song

            if kwargs.get("sender") != Song:
                return
            self._init_song_select()

        post_save.connect(update_song_list)
        post_delete.connect(update_song_list)

    def _init_song_select(self):
        from carillon.models import Song

        songs = Song.objects.values_list("name", flat=True)
        info = SelectInfo(
            name=gettext("Song"),
            options=songs,
            device=self.device,
            unique_id="song_selection",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def on_change(client: Client, userdata, message: MQTTMessage):
            song_name = message.payload.decode()
            try:
                song = Song.objects.get(name=song_name)
                self._selected_song = song
                self.song_select.select_option(song_name)
            except Song.DoesNotExist:
                self._selected_song = None

        self.song_select = Select(settings, on_change)
        self.song_select.write_config()
        if songs:
            self.song_select.select_option(songs[0])
            self._selected_song = Song.objects.get(name=songs[0])

    def _init_play_button(self):
        info = ButtonInfo(
            name=gettext("Play selected song"),
            device=self.device,
            unique_id="play_selected_song",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def on_press(client: Client, userdata, message: MQTTMessage):
            if message.payload.decode() == "PRESS" and self._selected_song:
                from carillon.models import Carillon

                carillon = Carillon.get_default()
                if not carillon:
                    return
                carillon.play(self._selected_song.midi, priority=self._priority)

        self.play_button = Button(settings, on_press)
        self.play_button.write_config()

    def _init_stop_button(self):
        info = ButtonInfo(
            name=gettext("Stop"),
            device=self.device,
            unique_id="stop_playing_song",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def on_press(client: Client, userdata, message: MQTTMessage):
            if message.payload.decode() == "PRESS":
                from carillon.models import Carillon

                carillon = Carillon.get_default()
                if not carillon:
                    return
                carillon.stop()

        self.stop_button = Button(settings, on_press)
        self.stop_button.write_config()

    def _init_priority_number(self):
        info = NumberInfo(
            name=gettext("Play priority"),
            device=self.device,
            unique_id="play_priority",
            min=-100,
            max=100,
            step=1,
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def on_change(client: Client, userdata, message: MQTTMessage):
            try:
                priority = int(message.payload.decode())
                self._priority = priority
                self.priority_number.set_value(priority)
            except ValueError:
                pass

        self.priority_number = Number(settings, on_change)
        self.priority_number.set_value(0)
