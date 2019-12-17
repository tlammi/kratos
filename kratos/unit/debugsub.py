"""
Debug MQTT Subscriber.
"""
import logging
import argparse
import mqttengine as mqtt
import util

LOGGER = logging.getLogger(__name__)

INCLUDE_FILTERS = []
EXCLUDE_FILTERS = []


@mqtt.topic_handler("$ENGINE/#")
@mqtt.topic_handler("#")
def printer(_client, _userdata, msg):
    """
    Printer callback for received messages
    """

    def matches(filter_list: list, topic):
        for f in filter_list:
            if util.mqtt_match(f, topic):
                return True
        return False

    if INCLUDE_FILTERS and not matches(INCLUDE_FILTERS, msg.topic):
        return

    if matches(EXCLUDE_FILTERS, msg.topic):
        return

    LOGGER.info("%s: %s", msg.topic, msg.payload)


def parse_cmdline():
    """
    Parses command line arguments

    :return: Parsed argument object
    """

    parser = argparse.ArgumentParser(
        description="""Unit used for debugging MQTT connection.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "-a", "--address", help="Broker address", default="localhost")
    parser.add_argument(
        "-p", "--port", type=int, help="Broker port", default="1883"
    )
    parser.add_argument(
        "-b", "--bind",
        help="Bind to local network interface, "
        "empty string means automatic", default=""
    )
    parser.add_argument(
        "-i", "--include",
        help="Include filter for received topics. "
        "Does not affect the subcriptions, only message display",
        action="append", default=[])

    parser.add_argument(
        "-e", "--exclude",
        help="Exclude filter for received topics. "
        "Does not affect the subcriptions, only message display",
        action="append", default=[])

    args = parser.parse_args()
    return args


def main():
    """
    Entrypoint
    """

    # TODO: Remove these once MqttEngine supports setting userdata
    global INCLUDE_FILTERS
    global EXCLUDE_FILTERS

    args = parse_cmdline()
    INCLUDE_FILTERS = args.include
    EXCLUDE_FILTERS = args.exclude

    logging.basicConfig(format="%(message)s")
    LOGGER.setLevel(logging.DEBUG)
    mqtt.engine().connect(args.address, args.port, bind_addr=args.bind)
    mqtt.engine().exec()


if __name__ == "__main__":
    main()
