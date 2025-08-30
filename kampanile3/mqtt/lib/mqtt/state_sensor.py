"""Binary sensor to reflect if the carillon is currently playing"""

from carillon.signals import carillon_play, carillon_stop
from django.utils.translation import gettext
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo

from .module import Module


class StateSensor(Module):
    def init_sensors(self):
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
