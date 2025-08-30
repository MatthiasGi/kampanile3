import os

from django.apps import AppConfig


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"

    def ready(self):
        if os.environ.get("MQTT"):
            self._setup_mqtt()

    def _setup_mqtt(self):
        from .lib.mqtt import Jukebox, StateSensors, device_info, mqtt_settings

        # Binary sensor to show whether the carillon is currently playing
        StateSensors(device_info, mqtt_settings)

        # Jukebox funcationality to play songs selected via MQTT
        Jukebox(device_info, mqtt_settings)
