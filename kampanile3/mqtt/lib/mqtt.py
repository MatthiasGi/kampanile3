import json
import logging

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

logger = logging.getLogger(__name__)


class MQTTMessage:
    """A simple wrapper for MQTT messages."""

    def __init__(self, topic, payload):
        self.topic = topic
        self.value = payload.decode()

    @property
    def text(self):
        return self.value

    @property
    def json(self):
        try:
            return json.loads(self.value)
        except ValueError:
            return None

    def __str__(self):
        return f"MQTTMessage(topic={self.topic}, value={self.value})"


class MQTTClient:
    """A simple wrapper for the MQTT client that allows subscribing to topics with callbacks."""

    def __init__(
        self, client_id, broker, port=1833, username=None, password=None, basetopic=""
    ):
        self.basetopic = basetopic
        self._subscriptions = {}

        self._client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
            clean_session=False,
        )
        if username and password:
            self._client.username_pw_set(username, password)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.logger = logger
        self._client.connect(broker, port)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            logger.info("Connected successfully to MQTT broker.")
        else:
            logger.error(f"Failed to connect to MQTT broker, return code {rc}.")

    def _on_message(self, client, userdata, message):
        logger.info(
            f"Message received on topic {message.topic}: {message.payload.decode()}"
        )
        if message.topic not in self._subscriptions:
            logger.warning(f"No callback registered for topic {message.topic}")
            return
        callback = self._subscriptions[message.topic]
        topic = (
            message.topic.removeprefix(f"{self.basetopic}/")
            if self.basetopic
            else message.topic
        )
        callback(MQTTMessage(topic, message.payload))

    def subscribe(self, callback, *topics):
        for t in topics:
            topic = f"{self.basetopic}/{t}" if self.basetopic else t
            self._subscriptions[topic] = callback
            self._client.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")

    def unsubscribe(self, *topics):
        for t in topics:
            topic = f"{self.basetopic}/{t}" if self.basetopic else t
            if topic in self._subscriptions:
                del self._subscriptions[topic]
                self._client.unsubscribe(topic)
                logger.info(f"Unsubscribed from topic: {topic}")
