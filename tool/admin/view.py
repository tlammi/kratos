import curses

class View:

    def __init__(self, curses_win):
        self._win = curses_win

    def refresh(self):
        self._win.addstr(0, 0, "hello")
        self._win.refresh()
        self._win.getkey()

    @classmethod
    def from_curses(cls, curses_win):
        return cls(curses_win)

    @classmethod
    def from_coords(cls, x, y, w, h):
        return cls(curses.newwin(h, w, y, x))
