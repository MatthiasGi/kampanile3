from django.conf import settings

from . import lib

urlpatterns = []

if settings.RUNNING_SERVER and settings.MQTT_HOST:
    lib.init_mqtt()
