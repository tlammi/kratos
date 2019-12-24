"""
Unit for handling one or more judge button pairs
"""
import argparse

import button
import mqttengine as mqtt


VALID_BUTTONS = ["TK"]
VALID_JUDGES = ["LEFT", "RIGHT", "MIDDLE"]


def button_handler(userdata: tuple):
    """
    Callback for button events

    :param userdata: Tuple of topic and payload to publish
    """
    topic, payload = userdata
    mqtt.engine().publish(topic, payload, 2)


def construct_tk_buttons(judges: list):
    """
    Constructs tkinter buttons

    :param judges: List of strings telling what buttons are handled by this unit
    """
    if "LEFT" in judges:
        b = button.TkButton(button.TkButtonPlace.RIGHT_U, "", "white")
        b.configure(("judge/vote/left", "w"), button_handler)
        b = button.TkButton(button.TkButtonPlace.RIGHT_D, "", "red")
        b.configure(("judge/vote/left", "r"), button_handler)
    if "MIDDLE" in judges:
        b = button.TkButton(button.TkButtonPlace.MIDDLE_U, "", "white")
        b.configure(("judge/vote/middle", "w"), button_handler)
        b = button.TkButton(button.TkButtonPlace.MIDDLE_D, "", "red")
        b.configure(("judge/vote/middle", "r"), button_handler)
    if "RIGHT" in judges:
        b = button.TkButton(button.TkButtonPlace.LEFT_U, "", "white")
        b.configure(("judge/vote/right", "w"), button_handler)
        b = button.TkButton(button.TkButtonPlace.LEFT_D, "", "red")
        b.configure(("judge/vote/right", "r"), button_handler)


def add_cli_args(parser: argparse.ArgumentParser) -> None:
    """
    Adds unit specific CLI args to argument parser

    :param parser: CLI parser
    """
    parser.add_argument("judges", help="Judges provided by this unit. One of "
                        "LEFT, MIDDLE, RIGHT. Multiple can be specified "
                        "with comma separated list")
    parser.add_argument(
        "buttontype", help="Specify button type to be used. "
        "Supported values (case-insensitive): [Tk]")


def run(args: argparse.Namespace) -> None:
    """
    Entrypoint for the unit

    :param args: Arguments parsed from the CLI
    """
    if args.buttontype.upper() not in VALID_BUTTONS:
        raise ValueError("Unsupported button type: %s" % args.buttontype)

    for j in args.judges.split(","):
        if j not in VALID_JUDGES:
            raise ValueError("Unknown judge position: %s" % j)

    judges = args.judges.split(",")

    # TODO: Change this after MqttEngine support posting to multiple heartbeats
    mqtt.engine().configure(mqtt.MqttEngineConfig("judge"))
    mqtt.engine().connect(args.address, args.port, bind_addr=args.bind)
    mqtt.engine().start()
    if args.buttontype.upper() == "TK":
        construct_tk_buttons(judges)
        button.TkButton.loop()

    mqtt.engine().stop()
