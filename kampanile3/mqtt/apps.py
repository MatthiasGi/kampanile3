from django.apps import AppConfig
from django.conf import settings


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"

    def ready(self):
        if settings.MQTT:
            self._setup_mqtt()

    def _setup_mqtt(self):
        from .lib import Jukebox, StateSensors, device_info, mqtt_settings

        # Binary sensor to show whether the carillon is currently playing
        StateSensors(device_info, mqtt_settings)

        # Jukebox funcationality to play songs selected via MQTT
        Jukebox(device_info, mqtt_settings)
