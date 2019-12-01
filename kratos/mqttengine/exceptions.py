"""
Exceptions used with MQTT engine
"""


class MqttException(Exception):
    """
    Base MQTT exception
    """


class NotConnectedError(MqttException):
    """
    Raised when a method is called when a connection
    is required but not present
    """


class QueueFullError(MqttException):
    """
    Raised when send buffer is full
    """
