"""
Platform screen unit capable of displaying current lifter's
name, lot number, team, attempt number, and loaded weight,
This unit also handles attempt time management and displays the
judging results.
"""
import argparse
import dataclasses
import enum
import time

import mqttengine as mqtt
import gui
import util.timer


class LiftJudging(enum.Enum):
    NOT_VALID = enum.auto()
    GOOD_LIFT = "white"
    NOT_GOOD_LIFT = "red"

@dataclasses.dataclass
class Judgings:
    left: LiftJudging
    middle: LiftJudging
    right: LiftJudging

@dataclasses.dataclass
class ClockTimer:
    timer: util.timer.Timer
    start_value: int


UNIT_NAME = "platform"

def parse_float_or(string: str, default: float = None) -> float:
    try:
        res = float(string)
    except ValueError:
        res = default or 0.0
    return res

def parse_int_or(string: str, default: int = None) -> int:
    try:
        res = int(string)
    except ValueError:
        res = int(parse_float_or(string, default))
    return res

def set_clock_time(screen_data_handle: gui.PlatformData,
                   seconds: int):
    minutes = int(seconds / 60)
    screen_data_handle.minutes = minutes
    screen_data_handle.seconds = seconds - minutes*60

def convert_judging(judging: LiftJudging) -> str:
    res = "NA"
    if judging == LiftJudging.GOOD_LIFT:
        res = "white"
    if judging == LiftJudging.NOT_GOOD_LIFT:
        res = "red"
    return res


@mqtt.topic_handler("lifter/current/#", UNIT_NAME)
def lifter_handler(_, userdata, msg):
    screen_data, _, _ = userdata

    topic = msg.topic.replace("lifter/current/", "")
    path = topic.split("/")

    if path[0] == "name":
        if path[1] == "first":
            screen_data.firstname = msg.payload.decode("utf-8")
        elif path[1] == "family":
            screen_data.lastname = msg.payload.decode("utf-8")
    elif path[0] == "barweight":
        val = parse_float_or(msg.payload, 0.0)
        if val > 0:
            screen_data.weight = val
    elif path[0] == "liftnumber":
        val = parse_int_or(msg.payload, 0)
        if val > 0 and val < 5:
            screen_data.attempt_num = val

@mqtt.topic_handler("clock/#", UNIT_NAME)
def clock_handler(client, userdata, msg):
    screen_data, clock, _ = userdata

    def once_per_second(remaining):
        nonlocal screen_data
        set_clock_time(screen_data, remaining - 1)

    def expired():
        nonlocal screen_data, client

        client.publish("clock/expired", None)

        for _ in range(0, 5):
            screen_data.minutes = None
            screen_data.seconds = None
            time.sleep(0.3)
            screen_data.minutes = 0
            screen_data.seconds = 0
            time.sleep(0.3)

        set_clock_time(screen_data, clock.start_value)

    topic = msg.topic.replace("clock/", "")
    path = topic.split("/")

    if path[0] == "start":
        if not clock.timer.running:
            countdown_value = (clock.timer.remaining_time if clock.timer.remaining_time > 0
                               else clock.start_value)
            clock.timer.start(countdown_value, once_per_second, expired)
    elif path[0] == "stop":
        if clock.timer.running:
            clock.timer.stop()
    elif path[0] == "time":
        if path[1] == "set":
            if clock.timer.running:
                return
            value = parse_int_or(msg.payload, 0)
            if value > 0:
                clock.start_value = value
                set_clock_time(screen_data, clock.start_value)
                clock.timer.clear()
        elif path[1] == "refresh":
            value = (clock.timer.remaining_time if clock.timer.remaining_time > 0
                     else clock.start_value)
            client.publish("clock/time/current", value)

@mqtt.topic_handler("judge/vote/#", UNIT_NAME)
def voting_result_handler(_, userdata, msg):
    screen_data, _, judgings = userdata

    position = msg.topic.replace("judge/vote/", "")
    if position in ("left", "middle", "right"):
        color = msg.payload.decode("utf-8")
        if color in ("red", "white"):
            setattr(judgings, position, LiftJudging(color))
        else:
            return

    red, white = (0, 0)
    for position in ("left", "middle", "right"):
        if getattr(judgings, position) == LiftJudging.GOOD_LIFT:
            white += 1
        elif getattr(judgings, position) == LiftJudging.NOT_GOOD_LIFT:
            red += 1

    if red >= 2 or white >= 2:
        screen_data.set_judging(left=convert_judging(judgings.left),
                                middle=convert_judging(judgings.middle),
                                right=convert_judging(judgings.right))

        if red + white == 3:
            time.sleep(3)
            screen_data.clear_judging()
            for position in ("left", "middle", "right"):
                setattr(judgings, position, LiftJudging.NOT_VALID)


def add_cli_args(parser: argparse.ArgumentParser) -> None:
    """
    Add unit specific arguments to the parser.

    :param parser: cli parser
    """

    parser.add_argument("-w", "--window",
                        help="Choose the type of window to launch",
                        metavar="[window, framebuffer]")

def run(args: argparse.Namespace) -> None:
    """
    Unit entrypoint.

    Sets the clock to the default countdown value and starts an mqtt client.

    :param args: arguments passed via cli
    """

    if args.window == "window":
        screen = gui.VirtualPlatformScreen()
    elif args.window == "framebuffer":
        screen = gui.PlatformScreen()
    else:
        raise RuntimeError("Invalid window type")

    judgings = Judgings(left=LiftJudging.NOT_VALID,
                        middle=LiftJudging.NOT_VALID,
                        right=LiftJudging.NOT_VALID)
    clock = ClockTimer(timer=util.timer.Timer(), start_value=60)

    set_clock_time(screen.data, clock.start_value)

    mqtt.engine().configure(mqtt.MqttEngineConfig(UNIT_NAME,
                                                  (screen.data,
                                                   clock,
                                                   judgings)))
    mqtt.engine().connect(args.address, args.port, bind_addr=args.bind)
    mqtt.engine().start()
    screen.run()
    mqtt.engine().stop()
