from abc import ABC, abstractmethod

from ha_mqtt_discoverable import DeviceInfo, Settings


class Module(ABC):
    def __init__(self, device_info: DeviceInfo, mqtt_settings: Settings.MQTT):
        self.device = device_info
        self.mqtt_settings = mqtt_settings
        self.init_sensors()

    @abstractmethod
    def init_sensors(self):
        pass
