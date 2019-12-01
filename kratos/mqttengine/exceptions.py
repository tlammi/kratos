
class MqttException(Exception):
    pass


class NotConnectedError(MqttException):
    pass


class QueueFullError(MqttException):
    pass
