"""
Entrypoint for kratos units
"""

import sys
import os
import argparse
import typing
from dataclasses import dataclass

# This enables both direct and "-m" invocation of kratos
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import unit.debugsub
import unit.judge
import unit.web


@dataclass
class Unit:
    add_cli_args: typing.Callable[[argparse.ArgumentParser], None]
    run: typing.Callable[[argparse.Namespace], None]
    helpstr: str


UNITS = {
    "debugsub": Unit(unit.debugsub.add_cli_args, unit.debugsub.run,
                     "Run debug client for monitoring MQTT traffic."),
    "judge": Unit(unit.judge.add_cli_args, unit.judge.run,
                  "Run judge unit"),
    "webserver": Unit(unit.web.add_cli_args, unit.web.run, "Run web server")
}


def parse_cli():
    """
    Parse command line

    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="""Competition management system
                    based on MQTT """,
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

    subparsers = parser.add_subparsers(
        dest="unit", title="units",
        metavar="[" + ", ".join(UNITS.keys()) + "]")

    subparsers.required = True

    for key, value in UNITS.items():
        subparser = subparsers.add_parser(key, help=value.helpstr)
        value.add_cli_args(subparser)
    args = parser.parse_args()

    return args


def main():
    args = parse_cli()
    UNITS[args.unit].run(args)


if __name__ == "__main__":
    main()
