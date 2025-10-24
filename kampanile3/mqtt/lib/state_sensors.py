"""General sensors representing the state of the default carillon."""

from carillon.models import Carillon
from carillon.signals import carillon_play, carillon_stop
from django.db.models.signals import post_save
from django.utils.translation import gettext
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import (
    BinarySensor,
    BinarySensorInfo,
    Number,
    NumberInfo,
    Switch,
    SwitchInfo,
)
from paho.mqtt.client import Client, MQTTMessage

from .module import Module


class StateSensors(Module):
    def init_sensors(self):
        self._init_playing_sensor()
        self._init_active_switch()
        self._init_volume_number()

    def _init_playing_sensor(self):
        info = BinarySensorInfo(
            name=gettext("Playing"),
            device_class="running",
            device=self.device,
            unique_id="playing",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        self.playing_sensor = BinarySensor(settings)
        self.playing_sensor.off()

        def update_sensor(state, **kwargs):
            if kwargs.get("carillon").default:
                self.playing_sensor.update_state(state)

        carillon_play.connect(lambda **kwargs: update_sensor(True, **kwargs))
        carillon_stop.connect(lambda **kwargs: update_sensor(False, **kwargs))

    def _init_active_switch(self):
        info = SwitchInfo(
            name=gettext("Active"),
            device=self.device,
            unique_id="active",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def publish_state():
            carillon = Carillon.get_default()
            if carillon and carillon.active:
                self.active_switch.on()
            else:
                self.active_switch.off()

        def on_change(client: Client, userdata, message: MQTTMessage):
            payload = message.payload.decode().lower()
            active = payload in ("1", "true", "on", "yes")

            carillon = Carillon.get_default()
            if not carillon:
                return
            carillon.active = active
            carillon.save()
            publish_state()

        self.active_switch = Switch(settings, on_change)
        publish_state()

        def update_active_switch(**kwargs):
            if kwargs.get("sender") == Carillon:
                publish_state()

        post_save.connect(update_active_switch)

    def _init_volume_number(self):
        info = NumberInfo(
            name=gettext("Volume"),
            device=self.device,
            unique_id="volume",
            min=0,
            max=127,
            step=1,
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def on_change(client: Client, userdata, message: MQTTMessage):
            try:
                carillon = Carillon.get_default()
                if not carillon:
                    return
                carillon.volume = int(message.payload.decode())
                carillon.save()
                self.volume_number.set_value(carillon.volume)
            except ValueError:
                pass

        def publish_state():
            carillon = Carillon.get_default()
            if not carillon:
                return
            self.volume_number.set_value(carillon.volume)

        self.volume_number = Number(settings, on_change)
        self.volume_number.write_config()
        publish_state()

        def update_volume(**kwargs):
            if kwargs.get("sender") == Carillon:
                publish_state()

        post_save.connect(update_volume)
