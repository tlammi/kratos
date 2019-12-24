"""
Abstract base class for all buttons
"""

import abc


class Button(abc.ABC):
    """
    Abstract base class for all buttons
    """

    @abc.abstractmethod
    def configure(self, userdata, callback: callable):
        """
        Configures a button.

        :param userdata: User specified data passed to callbacks
        :param callback: Event handler called when a button is pressed.
            Has prototype of callback(userdata)
        """

    @abc.abstractclassmethod
    def loop(cls):
        """
        Starts button listening functionality

        Should not return during normal functionality
        """
