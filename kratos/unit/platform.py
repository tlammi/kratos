import argparse

import gui


def add_cli_args(parser: argparse.ArgumentParser) -> None:
    """
    Add unit specific arguments to the parser.

    :param parser: cli parser
    """

    parser.add_argument("virtual", help="Specifiying virtual launches the GUI in a window",
                        action="store_true")

def run(args: argparse.Namespace) -> None:
    """
    Unit entrypoint

    :param args: arguments passed via cli
    """
    if args.virtual:
        screen = gui.VirtualPlatformScreen()
    else:
        raise RuntimeError("Not implemented")

    screen.run()