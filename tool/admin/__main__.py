
import window
import promptwindow
import curses


def mqtt_handler(*args):
    print("cb: ", args)


def echo_handler(argstr, outwin: window.Window):
    outwin.add_line(argstr)

def main(stdscr):
    TERM_WIDTH = curses.COLS
    TERM_HEIGHT = curses.LINES
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    outwin = window.Window.from_coords(0, 0, TERM_WIDTH, TERM_HEIGHT - 2)
    separator = window.Window.from_coords(0, TERM_HEIGHT - 2, TERM_WIDTH, 1)
    inwin = promptwindow.PromptWindow.from_coords(0, TERM_HEIGHT-1, TERM_WIDTH)

    mqtt = inwin.command_root.add_sub_command("mqtt", None)
    mqtt.add_sub_command("connect", mqtt_handler)
    inwin.command_root.add_sub_command("echo", echo_handler, outwin)
    separator.add_line(" "*(TERM_WIDTH-1), 1)

    while True:
        s = inwin.command_prompt()
        #outwin.add_line(s)

if __name__ == "__main__":
    curses.wrapper(main)
