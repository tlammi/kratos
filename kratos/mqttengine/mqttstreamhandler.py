"""
Class for passing logs to mqtt broker
"""
import logging


class MqttStreamHandler(logging.StreamHandler):
    """
    Stream handler for passing logs to MQTT
    """

    def __init__(self, engine, unitname="anon"):
        """
        Ctor

        :param engine: Handle to MqttEngine singlegton
        :param unitname: Unit under which the logs are placed
        """
        super().__init__()
        self._engine = engine
        self._unitname = unitname

    def emit(self, record):
        """
        Handles logging, called by logger

        Forwards logs received from logger to the correct topic
        in the MQTT broker.
        """
        msg = self.format(record)
        self._engine.publish("$ENGINE/%s/%s" %
                             (record.levelname.lower(), self._unitname), msg)
