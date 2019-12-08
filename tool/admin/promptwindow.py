
import enum
import curses
import exceptions


class ControlKey(enum.Enum):
    KEY_ESC = 0
    KEY_LEFT = 1
    KEY_RIGHT = 2
    KEY_UP = 3
    KEY_DOWN = 4
    KEY_BACKSPACE = 5

class PromptWindow:

    CONTROL_KEYS = {
        (27, 91, 68): ControlKey.KEY_LEFT,
        (27, 91, 67): ControlKey.KEY_RIGHT,
        (27, 91, 66): ControlKey.KEY_DOWN,
        (27, 91, 65): ControlKey.KEY_UP,
        (27,): ControlKey.KEY_ESC,
        (127,): ControlKey.KEY_BACKSPACE
    }

    def __init__(self, curses_win):
        self._win = curses_win
        self._buf = ""

    @classmethod
    def from_coords(cls, x: int, y: int, w: int):
        return cls(curses.newwin(1, w, y, x))

    def control_prompt(self):
        while True:
            c = self.next_key()

            if c in self.CONTROL_KEYS:
                ctrl = self.CONTROL_KEYS[c]
                if ctrl == ControlKey.KEY_ESC:
                    raise exceptions.ModeChange()

    def command_prompt(self):
        while True:
            c = self.next_key()
            #print("buf:",c)
            if c == (ord('\n'),):
                res = self._buf
                self._buf = ""
                self._win.erase()
                self._win.refresh()
                return res
            elif c in self.CONTROL_KEYS:
                ctrl = self.CONTROL_KEYS[c]
                if ctrl == ControlKey.KEY_ESC:
                    raise exceptions.ModeChange()
                if ctrl == ControlKey.KEY_LEFT:
                    y, x = self._win.getyx()
                    if x > 0:
                        self._win.move(y, x-1)
                elif ctrl == ControlKey.KEY_BACKSPACE:
                    y, x = self._win.getyx()
                    if x > 0:
                        self._buf = self._buf[:x-1] + self._buf[x:]
                        self._win.delch(y, x-1)
                        self._win.move(y, x-1)
            else:
                y, x = self._win.getyx()
                if x >= len(self._buf):
                    self._buf += bytes(c).decode()
                else:
                    self._buf = self._buf[:x] + bytes(c).decode() + self._buf[x:]
                #print("buf:", self._buf)
                self._win.addstr(0, 0, self._buf)
                self._win.move(y, x+1)
                self._win.refresh()

    def next_key(self):
        buf = []
        # First character get is blocking
        c = self._win.getch()
        try:
            # To non-blocking mode
            self._win.nodelay(1)
            while True:
                buf.append(c)
                c = self._win.getch()
                if c == -1:
                    break
        finally:
            # To blocking mode
            self._win.nodelay(0)
        return tuple(buf)
