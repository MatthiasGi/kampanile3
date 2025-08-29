from directorium import Directorium

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-sze7ee3p!19w+$k8^8m64*8l@*+pr59gk+!mpus143_^94y&x1"

ALLOWED_HOSTS = []

LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"

# The Directorium instance used for the corresponding conditions of the
# `carillon.models.Rule` model.
DIRECTORIUM = Directorium.from_cache()

# MQTT-Settings
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_USERNAME = None
MQTT_PASSWORD = None

MQTT_DEVICE_NAME = "Kampanile"
MQTT_DEVICE_IDENTIFIERS = "kampanile"
