"""
Button implementation using tkinter. Mainly used for development/debugging
"""

import tkinter
import abc
import enum

from . import button


class TkButtonPlace(enum.Enum):
    """
    Button placement in GUI
    """
    LEFT_U = 0
    LEFT_D = 1
    MIDDLE_U = 2
    MIDDLE_D = 3
    RIGHT_U = 4
    RIGHT_D = 5


class TkButtonMeta(abc.ABCMeta):
    """
    Metaclass for TkButton. Provides class attributes.
    """

    def __new__(cls, *args, **kwargs):
        """
        Constructor

        All parameters are Python magic
        """
        cls._tk = tkinter.Tk()
        cls._left = tkinter.Frame(cls._tk)
        # Order is from the competitor's perspetive
        cls._left.pack(side="left")
        cls._middle = tkinter.Frame(cls._tk)
        cls._middle.pack(side="left")
        cls._right = tkinter.Frame(cls._tk)
        cls._right.pack(side="left")
        return super().__new__(cls, *args, **kwargs)

    def _register_button(cls, place: TkButtonPlace, text: str,
                         userdata, callback: callable, bground=None, fground=None):
        """
        Registers button to tkinter
        :param place: Where to place the button
        :param text: Button text
        :param userdata: Userdata passed to the callback
        :param callback: Callback called when button is pressed
        :param bground: Background color as string
        :param fground: Foreground color as string
        """
        placements = {
            TkButtonPlace.LEFT_U: (cls._left, "top"),
            TkButtonPlace.LEFT_D: (cls._left, "bottom"),
            TkButtonPlace.MIDDLE_U: (cls._middle, "top"),
            TkButtonPlace.MIDDLE_D: (cls._middle, "bottom"),
            TkButtonPlace.RIGHT_U: (cls._right, "top"),
            TkButtonPlace.RIGHT_D: (cls._right, "bottom"),
        }

        b = tkinter.Button(placements[place][0], bg=bground, fg=fground)
        b.pack(side=placements[place][1])

        b["text"] = text
        b["command"] = lambda: callback(userdata)


class TkButton(button.Button, metaclass=TkButtonMeta):
    """
    Virtual button based on tkinter
    """

    def __init__(self, place: TkButtonPlace, text: str, bground=None, fground=None):
        """
        Init

        :param place: Where to place the button
        :param text: Button text
        :param bground: Background color as string
        :param fground: Foreground color as string
        """
        self._place = place
        self._text = text
        self._bg = bground
        self._fg = fground

    def configure(self, userdata, callback: callable):
        self.__class__._register_button(
            self._place, self._text, userdata, callback, self._bg, self._fg)

    @classmethod
    def loop(cls):
        cls._tk.mainloop()
