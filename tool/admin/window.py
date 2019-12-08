
import curses
import sys
import enum
import time


class Window:

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
