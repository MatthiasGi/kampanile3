from django.conf import settings
from ha_mqtt_discoverable import DeviceInfo, Settings

from .jukebox import Jukebox
from .module import Module
from .state_sensors import StateSensors

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

__all__ = ["mqtt_settings", "device_info", "Jukebox", "Module", "StateSensors"]
