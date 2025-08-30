"""General sensors representing the state of the default carillon."""

from carillon.signals import carillon_play, carillon_stop
from django.db.models.signals import post_save
from django.utils.translation import gettext
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import (
    BinarySensor,
    BinarySensorInfo,
    Switch,
    SwitchInfo,
)
from paho.mqtt.client import Client, MQTTMessage

from .module import Module


class StateSensors(Module):
    def init_sensors(self):
        self._init_playing_sensor()
        self._init_active_switch()

    def _init_playing_sensor(self):
        info = BinarySensorInfo(
            name=gettext("Carillon playing"),
            device_class="running",
            device=self.device,
            unique_id="carillon_playing",
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
            name=gettext("Carillon active"),
            device=self.device,
            unique_id="carillon_active",
        )
        settings = Settings(mqtt=self.mqtt_settings, entity=info)

        def publish_state():
            from carillon.models import Carillon

            carillon = Carillon.get_default()
            if carillon and carillon.active:
                self.active_switch.on()
            else:
                self.active_switch.off()

        def on_change(client: Client, userdata, message: MQTTMessage):
            from carillon.models import Carillon

            payload = message.payload.decode().lower()
            active = payload in ("1", "true", "on", "yes")
            try:
                carillon = Carillon.objects.get(default=True)
                carillon.active = active
                carillon.save()
                publish_state()
            except Carillon.DoesNotExist:
                pass

        self.active_switch = Switch(settings, on_change)
        publish_state()

        def update_active_switch(**kwargs):
            from carillon.models import Carillon

            if kwargs.get("sender") != Carillon:
                return
            publish_state()

        post_save.connect(update_active_switch)
