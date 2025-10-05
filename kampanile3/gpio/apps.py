import os
import threading
import time

from django.apps import AppConfig
from django.conf import settings


class GpioConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gpio"

    def ready(self):
        if (
            settings.RUNNING_SERVER
            and settings.GPIO
            and os.environ.get("RUN_MAIN") == "true"
        ):

            def load():
                time.sleep(3)  # Ensure that Django is fully started

                from .lib import init_thread

                init_thread()

            threading.Thread(target=load, daemon=True).start()
