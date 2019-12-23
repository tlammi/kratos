"""
Debug MQTT Subscriber.
"""
import logging
import argparse
import mqttengine as mqtt
import util

LOGGER = logging.getLogger(__name__)


@mqtt.topic_handler("$ENGINE/#")
@mqtt.topic_handler("#")
def printer(_client, userdata, msg):
    """
    Printer callback for received messages
    """

    include_filters = userdata[0]
    exclude_filters = userdata[1]

    def matches(filter_list: list, topic):
        for f in filter_list:
            if util.mqtt_match(f, topic):
                return True
        return False

    if include_filters and not matches(include_filters, msg.topic):
        return

    if matches(exclude_filters, msg.topic):
        return

    LOGGER.info("%s: %s", msg.topic, msg.payload)


def add_cli_args(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "-i", "--include",
        help="Include filter for received topics. "
        "Does not affect the subcriptions, only message display. "
        "Multiple can be specified.",
        action="append", default=[])

    parser.add_argument(
        "-e", "--exclude",
        help="Exclude filter for received topics. "
        "Does not affect the subcriptions, only message display."
        "Multiple can be specified.",
        action="append", default=[])


def run(args: argparse.Namespace) -> None:
    """
    Entrypoint
    """

    logging.basicConfig(format="%(message)s")
    LOGGER.setLevel(logging.DEBUG)
    mqtt.engine().configure(
        mqtt.MqttEngineConfig("debugsub", (args.include, args.exclude))
    )
    mqtt.engine().connect(args.address, args.port, bind_addr=args.bind)
    mqtt.engine().exec()
