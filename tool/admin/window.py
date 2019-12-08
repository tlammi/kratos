
import curses
import sys
import enum
import time


class InputType(enum.Enum):
    KEY_LEFT = 0
    KEY_RIGHT = 1
    KEY_UP = 2
    KEY_DOWN = 3
    KEY_ESC = 4

class Window:

    KEYPRESS_DELAY_S = 0.05
    CONTROL_KEY_MAPPINGS = {
        (27, 91, 68): InputType.KEY_LEFT,
        (27, 91, 67): InputType.KEY_RIGHT,
        (27, 91, 66): InputType.KEY_DOWN,
        (27, 91, 65): InputType.KEY_UP,
        (27,): InputType.KEY_ESC
    }

    def __init__(self, win, x: int, y: int, w: int, h: int):
        self._win = win
        self._topleft = (x, y)
        self._dims = (w, h)
        self._cur_line = 0
        self._buf = [""]*self._dims[1]
        self._in_control_mode = False

    @classmethod
    def from_coords(cls, x: int, y: int, w: int, h: int):
        return cls(curses.newwin(h, w, y, x), x, y, w, h)

    def prompt(self):
        c = self.next_key()
        print(c)

        return "Hwllo"

    def control_prompt(self):
        pass

    def command_prompt(self):
        while True:
            c = self.next_key()
            print(c)
            if c in self.CONTROL_KEY_MAPPINGS:
                # y, x = self._win.getyx()
                # if x >= len(self._buf):
                #     self._buf += bytes(c).decode()
                # else:
                #     self._buf = self._buf[:x] + bytes(c).decode() + self._buf[x:]
                # self._win.addstr(0, 0, self._buf)
                # self._win.move(y, x+1)
                # self._win.refresh()
                ctrl = self.CONTROL_KEY_MAPPINGS[c]
                if ctrl == InputType.KEY_ESC:
                    raise ModeChange()
            else:
                y, x = self._win.getyx()
                if x >= len(self._buf[y]):
                    self._buf[y] += bytes(c).decode()
                else:
                    self._buf[y] = self._buf[y][:x] + bytes(c).decode() + self._buf[y][x+1:]
                self._win.erase()
                self._win.addstr(y, 0, self._buf[y])
                self._win.refresh()

    def get_input(self):
        """
        res = ""
        while True:
            c = self._win.getch()
            if c == 10:
                break
            print("key:", c)
            res += chr(c)
        self._win.erase()
        self._win.refresh()
        return res
        """

        res = ""
        while True:
            c = self.next_key()

            if c in self.CONTROL_KEY_MAPPINGS:
                return self.CONTROL_KEY_MAPPINGS[c], res

            if c == 10:
                break
            res += c
        return res
        #string = self._win.getstr()
        #self._win.erase()
        #self._win.refresh()
        #return string

    def add_line(self, line: str, color_index=0):

        if self._cur_line >= self._dims[1]:
            self._buf = self._buf[1:] + [line]
            self._cur_line -= 1

        self._buf[self._cur_line] = line
        self._cur_line += 1
        self._win.erase()
        for i, l in enumerate(self._buf):
            self._win.addstr(i, 0, l, curses.color_pair(color_index))
        self._win.refresh()


class ModeChange(Exception):
    pass
