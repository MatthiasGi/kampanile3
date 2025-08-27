from directorium import Directorium
from mqtt.lib import MQTTClient

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-sze7ee3p!19w+$k8^8m64*8l@*+pr59gk+!mpus143_^94y&x1"

ALLOWED_HOSTS = []

LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"

# The Directorium instance used for the corresponding conditions of the
# `carillon.models.Rule` model.
DIRECTORIUM = Directorium.from_cache()

# MQTT-Settings
MQTT = MQTTClient(
    client_id="kampanile",
    broker="localhost",
    port=1883,
    username=None,
    password=None,
    basetopic="kampanile",
)
