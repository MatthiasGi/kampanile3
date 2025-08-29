import os

from carillon.signals import carillon_play, carillon_stop
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext
from ha_mqtt_discoverable import DeviceInfo, Settings
from ha_mqtt_discoverable.sensors import BinarySensor, BinarySensorInfo


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"

    def ready(self):
        if os.environ.get("MQTT"):
            self._setup_mqtt()

    def _setup_mqtt(self):
        mqtt_settings = Settings.MQTT(
            host=settings.MQTT_HOST,
            port=settings.MQTT_PORT,
            username=settings.MQTT_USERNAME,
            password=settings.MQTT_PASSWORD,
        )

        device_info = DeviceInfo(
            name=settings.MQTT_DEVICE_NAME,
            identifiers=settings.MQTT_DEVICE_IDENTIFIERS,
        )

        sensor_info = BinarySensorInfo(
            name=gettext("Carillon playing"),
            device_class="running",
            device=device_info,
            unique_id="carillon_playing",
        )
        sensor_settings = Settings(mqtt=mqtt_settings, entity=sensor_info)

        playing_sensor = BinarySensor(sensor_settings)
        playing_sensor.off()

        def update_playing_sensor(state, **kwargs):
            if kwargs.get("carillon").default:
                playing_sensor.update_state(state)

        carillon_play.connect(lambda **kwargs: update_playing_sensor(True, **kwargs))
        carillon_stop.connect(lambda **kwargs: update_playing_sensor(False, **kwargs))
