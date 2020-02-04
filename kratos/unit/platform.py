"""
Platform screen unit capable of displaying current lifter's
name, lot number, team, attempt number, and loaded weight,
This unit also handles attempt time management and displays the
judging results.
"""
import argparse
import enum
import time

import mqttengine as mqtt
import gui
import util.timer as timer


UNIT_NAME = "platform"

clock_start_value = 60
clock_timer = timer.Timer()

class LiftJudging(enum.Enum):
    NOT_VALID = enum.auto()
    GOOD_LIFT = "white"
    NOT_GOOD_LIFT = "red"

judgings = {
    "left": LiftJudging.NOT_VALID,
    "middle": LiftJudging.NOT_VALID,
    "right": LiftJudging.NOT_VALID
}


def parse_float_or(string: str, default: float=None) -> float:
    try:
        res = float(string)
    except:
        res = default if default else 0.0
    finally:
        return res

def parse_int_or(string: str, default: int=None) -> int:
    try:
        res = int(string)
    except:
        res = int(parse_float_or(string, default))
    finally:
        return res

def set_clock_time(screen_data_handle: gui.PlatformData,
                   seconds: int):
    minutes = int(seconds / 60)
    screen_data_handle.minutes = minutes
    screen_data_handle.seconds = seconds - minutes*60

def convert_judging(judging: LiftJudging) -> bool:
    if judging == LiftJudging.NOT_VALID:
        return None
    elif judging == LiftJudging.GOOD_LIFT:
        return True
    elif judging == LiftJudging.NOT_GOOD_LIFT:
        return False


@mqtt.topic_handler("lifter/current/#", UNIT_NAME)
def lifter_handler(client, userdata, msg):
    screen_data = userdata

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
    global clock_timer, clock_start_value
    screen_data = userdata

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

        set_clock_time(screen_data, clock_start_value)

    topic = msg.topic.replace("clock/", "")
    path = topic.split("/")

    if path[0] == "start":
        if not clock_timer.running:
            countdown_value = (clock_timer.remaining_time if clock_timer.remaining_time > 0
                                                          else clock_start_value)
            clock_timer.start(countdown_value, once_per_second, expired)
    elif path[0] == "stop":
        if clock_timer.running:
            clock_timer.stop()
    elif path[0] == "time":
        if path[1] == "set":
            if clock_timer.running:
                return
            value = parse_int_or(msg.payload, 0)
            if value > 0:
                clock_start_value = value
                set_clock_time(screen_data, clock_start_value)
                clock_timer.clear()
        elif path[1] == "refresh":
            value = (clock_timer.remaining_time if clock_timer.remaining_time > 0
                                                else clock_start_value)
            client.publish("clock/time/current", value)

@mqtt.topic_handler("judge/vote/#", UNIT_NAME)
def voting_result_handler(client, userdata, msg):
    global judgings
    screen_data = userdata

    topic = msg.topic.replace("judge/vote/", "")
    if topic in judgings:
        color = msg.payload.decode("utf-8")
        if color in ("red", "white"):
            judgings[topic] = LiftJudging(color)
        else:
            return

    red, white = (0, 0)
    for judging in judgings.values():
        if judging == LiftJudging.GOOD_LIFT:
            white += 1
        elif judging == LiftJudging.NOT_GOOD_LIFT:
            red += 1

    if red >= 2 or white >= 2:
        screen_data.set_judging(left=convert_judging(judgings["left"]),
                                middle=convert_judging(judgings["middle"]),
                                right=convert_judging(judgings["right"]))

        if red + white == 3:
            time.sleep(3)
            screen_data.clear_judging()
            for judging in judgings.values():
                judging = LiftJudging.NOT_VALID


def add_cli_args(parser: argparse.ArgumentParser) -> None:
    """
    Add unit specific arguments to the parser.

    :param parser: cli parser
    """

    parser.add_argument("--virtual",
                        help="Specifiying virtual, launches the GUI in a window",
                        action="store_true")

def run(args: argparse.Namespace) -> None:
    """
    Unit entrypoint.

    Sets the clock to the default countdown value and starts an mqtt client.

    :param args: arguments passed via cli
    """

    if args.virtual == True:
        screen = gui.VirtualPlatformScreen()
    else:
        screen = gui.PlatformScreen()

    set_clock_time(screen.data, clock_start_value)

    mqtt.engine().configure(mqtt.MqttEngineConfig(UNIT_NAME,
                                                  screen.data))
    mqtt.engine().connect(args.address, args.port, bind_addr=args.bind)
    mqtt.engine().start()
    screen.run()
    mqtt.engine().stop()