"""
MQTT engine configuration
"""
import logging
from dataclasses import dataclass


@dataclass
class MqttEngineConfig:
    """
    Config object passed to MqttEngine
    """

    # Name of the current unit, used e.g. for logs
    unit_name: str = "anon"
    # User data passed to MQTT event handlers
    userdata: tuple = None
    # If True, publish heartbeat messages
    send_heartbeat: bool = True
    # Heartbeat publish interval, ignored if not send_heartbeat
    heartbeat_interval_s: int = 60
    # Log level filter for MQTT publish (can be int or equivalent str)
    loglevel = logging.DEBUG
