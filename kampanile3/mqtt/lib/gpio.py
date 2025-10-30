from django.db.models.signals import post_delete, post_save
from gpio.models import Input
from gpio.signals import input_triggered
from ha_mqtt_discoverable import Settings
from ha_mqtt_discoverable.sensors import DeviceTrigger, DeviceTriggerInfo

from .module import Module


class GPIO(Module):
    def init_sensors(self):
        self._update_inputs()

        input_triggered.connect(lambda **kwargs: self._handle_input_triggered(**kwargs))
        post_save.connect(lambda **kwargs: self._update_inputs(), sender=Input)
        post_delete.connect(lambda **kwargs: self._update_inputs(), sender=Input)

    def _update_inputs(self):
        self._triggers = {}
        for input in Input.objects.filter(active=True):
            info = DeviceTriggerInfo(
                name=input.name,
                type="button_short_press",
                subtype=input.name,
                unique_id=f"gpio_trigger_{input.pk}",
                device=self.device,
            )
            settings = Settings(mqtt=self.mqtt_settings, entity=info)
            self._triggers[input.pk] = DeviceTrigger(settings)
            self._triggers[input.pk].write_config()

    def _handle_input_triggered(self, **kwargs):
        input = kwargs.get("input")
        if input and input.pk in self._triggers:
            self._triggers[input.pk].trigger(input.pin)
