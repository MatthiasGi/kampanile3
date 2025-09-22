import time
from threading import Thread

from django.apps import AppConfig
from django.conf import settings


class GpioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gpio"

    def ready(self):
        if settings.GPIO:
            self._setup_gpio()

    def _setup_gpio(self):
        from .models import Input

        Input.load_pins()
        thread = Thread(target=self._gpio_loop, daemon=True)
        thread.start()

    def _gpio_loop(self):
        from .models import Input

        while True:
            Input.check_pins()
            time.sleep(0.2)
