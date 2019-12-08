
import enum
import curses
import exceptions
import commandnode


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
        self._command_root = commandnode.CommandNode(None)

    @classmethod
    def from_coords(cls, x: int, y: int, w: int):
        return cls(curses.newwin(1, w, y, x))

    @property
    def command_root(self):
        return self._command_root

    def control_prompt(self):
        while True:
            c = self.next_key()

            if c in self.CONTROL_KEYS:
                ctrl = self.CONTROL_KEYS[c]
                if ctrl == ControlKey.KEY_ESC:
                    raise exceptions.ModeChange()

    def command_prompt(self):
        def handle_enter():
            # res = self._buf
            # self._buf = ""
            # self._win.erase()
            # self._win.refresh()
            # return res
            self._command_root.call(self._buf.split())
            self._buf = ""
            self._win.erase()
            self._win.refresh()

        def handle_tab():
            self._buf = " ".join(self._command_root.autocomplete(self._buf.split()))
            self._win.erase()
            self._win.addstr(0, 0, self._buf)
            self._win.refresh()

        def handle_ctrl_keys(key: ControlKey):
            if key == ControlKey.KEY_ESC:
                raise exceptions.ModeChange()
            if key == ControlKey.KEY_LEFT:
                y, x = self._win.getyx()
                if x > 0:
                    self._win.move(y, x-1)
            elif key == ControlKey.KEY_RIGHT:
                y, x = self._win.getyx()
                if x < len(self._buf) - 1:
                    self._win.move(y, x + 1)
            elif key == ControlKey.KEY_BACKSPACE:
                y, x = self._win.getyx()
                if x > 0:
                    self._buf = self._buf[:x-1] + self._buf[x:]
                    self._win.delch(y, x-1)
                    self._win.move(y, x-1)

        def handle_default(inbytes: tuple):
            y, x = self._win.getyx()
            if x >= len(self._buf):
                self._buf += bytes(inbytes).decode()
            else:
                self._buf = self._buf[:x] + bytes(inbytes).decode() + self._buf[x:]
            self._win.addstr(0, 0, self._buf)
            self._win.move(y, x+1)
            self._win.refresh()

        while True:
            c = self.next_key()
            #print("buf:",c)
            if c == (ord('\n'),):
                return handle_enter()
            if c == (ord('\t'),):
                handle_tab()
            elif c in self.CONTROL_KEYS:
                ctrl = self.CONTROL_KEYS[c]
                handle_ctrl_keys(ctrl)
            else:
                handle_default(c)

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



