
import window
import promptwindow
import commandnode
import curses


def mqtt_handler(*args):
    print("cb: ", args)


def help_handler(argstr, outwin: window.Window, root_node: commandnode.CommandNode):
    outwin.add_line("Supported commands:")
    cmds = root_node.subcommands_and_helps()
    for cmd, help_str in cmds.items():
        outwin.add_line("\t%s - %s" % (cmd, help_str))
    outwin.add_line("")
    outwin.add_line("Access commands for more help")
    outwin.add_line("")


def echo_handler(argstr, outwin: window.Window):
    outwin.add_line(argstr)


def main(stdscr):
    TERM_WIDTH = curses.COLS
    TERM_HEIGHT = curses.LINES
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    outwin = window.Window.from_coords(0, 0, TERM_WIDTH, TERM_HEIGHT - 2)
    separator = window.Window.from_coords(0, TERM_HEIGHT - 2, TERM_WIDTH, 1)
    inwin = promptwindow.PromptWindow.from_coords(0, TERM_HEIGHT-1, TERM_WIDTH)

    inwin.command_root.add_sub_command("help", "Prints help", help_handler, outwin, inwin.command_root)

    mqtt = inwin.command_root.add_sub_command("mqtt", "MQTT specific functionality", None)
    mqtt.set_handler(help_handler, outwin, mqtt)
    mqtt.add_sub_command("connect", "Connect to MQTT broker", mqtt_handler)
    inwin.command_root.add_sub_command("echo", "This echoes stuff", echo_handler, outwin)
    separator.add_line(" "*(TERM_WIDTH-1), 1)

    while True:
        s = inwin.command_prompt()

if __name__ == "__main__":
    curses.wrapper(main)
