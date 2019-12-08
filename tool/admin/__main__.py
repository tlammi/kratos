
import outwindow
import promptwindow
import commandnode
import curses


def mqtt_connect(arg):
    print("mqtt connect: ", arg)


def mqtt_disconnect(arg):
    print("mqtt disconnect: ", arg)

def mqtt_pub(arg):
    print("mqtt pub: ", arg)

def mqtt_sub(arg):
    print("mqtt sub: ", arg)

def help_handler(argstr, outwin: outwindow.OutWindow, root_node: commandnode.CommandNode):
    outwin.clear()
    outwin.add_line("Supported commands:")
    cmds = root_node.subcommands_and_helps()
    for cmd, help_str in cmds.items():
        outwin.add_line("\t%s - %s" % (cmd, help_str))
    outwin.add_line("")
    outwin.add_line("Access commands for more help")
    outwin.add_line("")


def echo_handler(argstr, outwin: outwindow.OutWindow):
    outwin.add_line(argstr)


def construct_command_tree(prompt_window: promptwindow.PromptWindow, help_window: outwindow.OutWindow):
    root = prompt_window.command_root
    root.add_subcommand("help", "Prints help", help_handler, help_window, root)

    mqtt = root.add_subcommand("mqtt", "Access MQTT specific commands", None)
    mqtt.set_handler(help_handler, help_window, mqtt)

    mqtt.add_subcommand("connect", "Connect to MQTT broker", mqtt_connect)
    mqtt.add_subcommand("disconnect", "Disconnect from MQTT broker", mqtt_disconnect)
    mqtt.add_subcommand("pub", "Publish to a topic, usage: mqtt pub <topic> <message>", mqtt_pub)
    mqtt.add_subcommand("sub", "Subscribe to a topic, usage: mqtt sub <topic_filter>", mqtt_sub)

    root.add_subcommand("echo", "Echoes arguments to output (used for testing)", echo_handler, help_window)

    unit = root.add_subcommand("unit", "Access unit specific commands", None)
    unit.set_handler(help_handler, help_window, unit)

    unit.add_subcommand("status", "Get status of a unit. Usage: unit status <name>", None)

def main(stdscr):
    TERM_WIDTH = curses.COLS
    TERM_HEIGHT = curses.LINES
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    outwin = outwindow.OutWindow.from_coords(0, 0, TERM_WIDTH, TERM_HEIGHT - 2)
    separator = outwindow.OutWindow.from_coords(0, TERM_HEIGHT - 2, TERM_WIDTH, 1)
    inwin = promptwindow.PromptWindow.from_coords(0, TERM_HEIGHT-1, TERM_WIDTH)

    construct_command_tree(inwin, outwin)
    inwin.set_default_command("help")
    separator.add_line(" "*(TERM_WIDTH-1), 1)

    while True:
        s = inwin.command_prompt()


if __name__ == "__main__":
    curses.wrapper(main)
