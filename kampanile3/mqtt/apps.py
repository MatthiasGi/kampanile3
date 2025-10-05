import os
import threading
import time

from django.apps import AppConfig
from django.conf import settings


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"

    def ready(self):
        if (
            settings.RUNNING_SERVER
            and settings.MQTT_HOST
            and os.environ.get("RUN_MAIN") == "true"
        ):

            def load():
                time.sleep(3)  # Ensure that Django is fully started

                from .lib import init_mqtt

                init_mqtt()

            threading.Thread(target=load, daemon=True).start()
