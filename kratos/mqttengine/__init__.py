"""
MQTT Engine

Export a singleton which provides functionality shared among the
all the clients

"""

from .__mqttengine import engine, topic_handler
from .exceptions import *
