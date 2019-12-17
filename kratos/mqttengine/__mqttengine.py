"""
MQTT Engine implementation
"""

import logging

import paho.mqtt.client as mqtt

from . import exceptions

LOGGER = logging.getLogger(__name__)


class MqttEngine:
    """
    Singleton class for managing MQTT clients
    """

    def __init__(self):
        self._handlers = {}
        self._client = mqtt.Client()
        self._keepalive_s = 0

    def connect(self, broker: str, port=1883, keepalive_s=60, bind_addr=""):
        """
        Connect to a broker

        :param broker: Address of the broker (domain or IP)
        :param port: Port to connect to
        :param keepalive_s: Heartbeat period
        :param bind_addr: Bind connection to local IP
        :return: None
        """
        self._client.on_message = self._msg_cb
        self._client.on_connect = self._connect_cb
        for filt, cb in self._handlers.items():
            self._client.message_callback_add(filt, cb)
        self._keepalive_s = keepalive_s
        self._client.connect(broker, port, keepalive_s, bind_addr)

    def disconnect(self):
        """
        Disconnects the client

        :return:
        """
        self._client.disconnect()

    def set_user_data(self, userdata):
        """
        Updates the userdata argument passsed to callbacks

        :param userdata: Data passed to callbacks
        """
        self._client.user_data_set(userdata)

    def topic_handler(self, topic_filter: str):
        """
        Decorator for adding topic handler

        :param topic_filter: Topic filter used for matching messages
        :return: Wrapper for the callback
        """
        def topic_handler_wrapper(func: callable):
            self._handlers[topic_filter] = func
            return func
        return topic_handler_wrapper

    def exec(self):
        """
        Execute the engine. Never returns
        :return:
        """
        self._client.loop_forever()

    def start(self):
        """
        Start engine in the background

        :return: None
        """
        self._client.loop_start()

    def stop(self):
        """
        Stop engine running in the background

        :return: None
        """
        self._client.loop_stop()

    def publish(self, topic: str, payload=None, qos=0, retain=False):
        """
        Publish message to a topic

        :param topic: Topic to publish to
        :param payload: Message payload. None means empty payload
        :param qos: Quality of service
            0 - Send but don't care if message reaches the target
            1 - Message is received at least 1 time
            2 - Message is received exactly 1 time

        :param retain: If True, will be set as "last known good" message
            for the topic
        :return: None

        :raises NotConnectedException: Connection has not been established
        :raises QueueFullError: Publish FIFO is full
        """
        res = self._client.publish(topic, payload, qos, retain)
        if res.rc == mqtt.MQTT_ERR_SUCCESS:
            res.wait_for_publish()
            return
        if res.rc == mqtt.MQTT_ERR_NO_CONN:
            raise exceptions.NotConnectedError(
                "Could not publish to topic %s" % topic)
        if res.rc == mqtt.MQTT_ERR_QUEUE_SIZE:
            raise exceptions.QueueFullError(
                "Send buffer is full, cannot publish.")
        raise ValueError("Unknown result code from paho-mqtt: %s" % res.rc)

    def _connect_cb(self, client, userdata, flags, rc):
        LOGGER.info("Connected with result code %s", rc)
        for topic in self._handlers:
            result, mid = client.subscribe(topic)
            if result == mqtt.MQTT_ERR_SUCCESS:
                LOGGER.info("Successfully subscribed to topic %s", topic)
            elif result == mqtt.MQTT_ERR_NO_CONN:
                raise exceptions.NotConnectedError("No connection established")
            else:
                raise ValueError("Unknown return value from paho-mqtt")

    def _disconnect_cb(self, client, userdata, rc):
        LOGGER.info("Disconnected")

    def _msg_cb(self, client, userdata, msg):
        LOGGER.debug("Message from topic: %s", msg.topic)


ENGINE = MqttEngine()


def engine():
    """
    Get MQTT engine singleton

    :return: Instance of MqttEngine
    """
    return ENGINE


def topic_handler(*args, **kwargs):
    """
    Wrapper for topic handler decorator

    :param args: Arguments passed forward
    :param kwargs: Keyword arguments passed forward
    :return: Wrapper for topic handler
    """
    return ENGINE.topic_handler(*args, **kwargs)
