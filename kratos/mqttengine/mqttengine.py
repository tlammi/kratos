
import paho.mqtt.client as mqtt

_handlers = {}
_client = None


def topic_handler(topic: str):
    global _handlers

    def topic_handler_wrapper(func):
        _handlers[topic] = func

    return topic_handler_wrapper


def _connect_callback(client, userdata, flags, rc):
    global _handlers
    print("Connected with result code: %s" % rc)
    for topic in _handlers:
        client.subscribe(topic)


def _publish_callback(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def init():
    global _client
    _client = mqtt.Client()


def connect(broker_ip: str, port=1883, timeout_s=60):
    global _client
    _client.connect(broker_ip, port, timeout_s)


def start():
    global _client
    _client.loop_start()


def stop():
    global _client
    _client.loop_stop()


def loop():
    global _client
    _client.loop_forever()
