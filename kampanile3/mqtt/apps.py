from django.apps import AppConfig
from django.conf import settings


class MqttConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mqtt"

    def ready(self):
        from carillon.models import Carillon, Song

        def play(msg):
            data = msg.json
            carillon_name = data.get("carillon", Carillon.objects.first().name)
            carillon = Carillon.objects.get(name=carillon_name)
            song = Song.objects.get(slug=data["song"])
            carillon.play(song.midi)

        mqtt = settings.MQTT
        mqtt.subscribe(play, "play")
