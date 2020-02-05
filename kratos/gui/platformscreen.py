"""
Platform screen for displaying information about the current lifter
and lift to the spotters/loaders and spectators
"""

import PyQt5.QtCore as QtCore

from .screen import Screen


class PlatformScreen(Screen):
    """
    Platform screen that runs on an eglfs surface i.e. no X Server is needed
    """

    def __init__(self):
        super().__init__(["-platform", "eglfs"])

        self._setup()

    @property
    def data(self):
        """
        Access the data displayed in the screen

        :return: PlatformData object for this screen
        """

        return self._data

    def _setup(self):
        self._data = PlatformData()
        self._view.rootContext().setContextProperty("applicationData", self._data)

        self._load("platform_view.qml")


class VirtualPlatformScreen(PlatformScreen):
    """
    Platform screen that runs on a "standard" application window
    """

    def __init__(self):
        super(PlatformScreen, self).__init__()

        self._setup()

    def reload(self):
        """
        Reload the QML resource file

        Usefull for development

        :return: None
        """

        self._view.engine().clearComponentCache()
        self._load("platform_view.qml")


class PlatformData(QtCore.QObject):
    """
    Model containing the data that's displayed on the platform screen
    """

    # pylint: disable=too-many-instance-attributes
    # It makes no sense to refactor this any further

    def __init__(self):
        super().__init__()

        self._lot_number = "-"
        self._firstname = "-"
        self._lastname = "-"
        self._team = "-"
        self._attempt_num = "-"
        self._weight = "-"
        self._minutes = "-"
        self._seconds = "-"
        self._judging = None

    _lot_numberChanged = QtCore.pyqtSignal(str,
                                           name="lot_numberChanged",
                                           arguments=["lot_number"])

    @QtCore.pyqtProperty(str, notify=_lot_numberChanged)
    def lot_number(self):
        """
        Read and write the lifter's lot number

        :param lot_number: The lot number as an interger
        :return: The current lot number as a string or "-"
        """
        return self._lot_number

    @lot_number.setter
    def lot_number(self, lot_number: int):
        self._lot_number = str(lot_number)
        self._lot_numberChanged.emit(self._lot_number)

    _firstnameChanged = QtCore.pyqtSignal(str,
                                          name="firstnameChanged",
                                          arguments=["firstname"])

    @QtCore.pyqtProperty(str, notify=_firstnameChanged)
    def firstname(self):
        """
        Read and write the lifter's first name

        :param firstname: The lifter's first name as a string
        :return: The current lifter's first name as a string or "-"
        """

        return self._firstname

    @firstname.setter
    def firstname(self, firstname: str):
        self._firstname = firstname
        self._firstnameChanged.emit(self._firstname)

    _lastnameChanged = QtCore.pyqtSignal(str,
                                         name="lastnameChanged",
                                         arguments=["lastname"])

    @QtCore.pyqtProperty(str, notify=_lastnameChanged)
    def lastname(self):
        """
        Read and write the lifter's last name

        :param lastname: The lifter's last name as a string
        :return: The current lifter's last name as a string or "-"
        """

        return self._lastname

    @lastname.setter
    def lastname(self, lastname: str):
        self._lastname = lastname
        self._lastnameChanged.emit(self._lastname)

    _teamChanged = QtCore.pyqtSignal(str,
                                     name="teamChanged",
                                     arguments=["team"])

    @QtCore.pyqtProperty(str, notify=_teamChanged)
    def team(self):
        """
        Read and write the lifter's team

        :param team: The lifter's team's name as a string
        :return: The current lifter's team's name as a string or "-"
        """

        return self._team

    @team.setter
    def team(self, team: str):
        self._team = team
        self._teamChanged.emit(self._team)

    _attempt_numChanged = QtCore.pyqtSignal(str,
                                            name="attempt_numChanged",
                                            arguments=["attempt"])

    @QtCore.pyqtProperty(str, notify=_attempt_numChanged)
    def attempt_num(self):
        """
        Read and write the attempt number

        Attempt numbers have to be positive. Setting attempt_num to 0 clears the
        field to default value of "-".

        :param attempt_num: The number of the current attempt as an interger
        :raises ValueError: If attempt_num is not a positive integer
        :return: The current attempt formated as a ordinal number string or "-"
        """

        return self._attempt_num

    @attempt_num.setter
    def attempt_num(self, attempt_num: int):
        if attempt_num < 0:
            raise ValueError("attempt_num has to be positive")

        if attempt_num == 1:
            self._attempt_num = "1st"
        elif attempt_num == 2:
            self._attempt_num = "2nd"
        elif attempt_num == 3:
            self._attempt_num = "3rd"
        elif attempt_num == 0:
            self._attempt_num = "-"
        else:
            # It's unlikely that we'd have more than 4 attempts, but hey who knows
            self._attempt_num = f"{attempt_num}th"

        self._attempt_numChanged.emit(self._attempt_num)

    _weightChanged = QtCore.pyqtSignal(str,
                                       name="weightChanged",
                                       arguments=["weight"])

    @QtCore.pyqtProperty(str, notify=_weightChanged)
    def weight(self):
        """
        Read and write the loaded weight

        :param weight: The currently loaded weight as a float
        :raises ValueError: If weight is not a positive float
        :return: The currently loaded weight as a string or "-"
        """

        return self._weight

    @weight.setter
    def weight(self, weight: float):
        if weight < 0:
            raise ValueError("weight has to be positive")
        self._weight = "-" if weight == 0 else str(weight)
        self._weightChanged.emit(self._weight)

    _minutesChanged = QtCore.pyqtSignal(str,
                                        name="minutesChanged",
                                        arguments=["minutes"])

    @QtCore.pyqtProperty(str, notify=_minutesChanged)
    def minutes(self):
        """
        Read and write the minutes of remaining time

        :param minutes: The minutes of remaining time as an integer
        :raises ValueError: If the value is negative
        :return: The current remaining minutes as a string or "-"
        """

        return self._minutes

    @minutes.setter
    def minutes(self, minutes: int):
        if minutes is None:
            self._minutes = "-"
        else:
            self._minutes = str(minutes)

        self._minutesChanged.emit(self._minutes)

    _secondsChanged = QtCore.pyqtSignal(str,
                                        name="secondsChanged",
                                        arguments=["seconds"])

    @QtCore.pyqtProperty(str, notify=_secondsChanged)
    def seconds(self):
        """
        Read and write the seconds of remaining time

        :param seconds: The seconds of remaining time as an integer
        :return: The current remaining seconds as a string or "-"
        """

        return self._seconds

    @seconds.setter
    def seconds(self, seconds: int):
        if seconds is None:
            self._seconds = "-"
        else:
            self._seconds = str(seconds) if seconds >= 10 else f"0{str(seconds)}"

        self._secondsChanged.emit(self._seconds)

    _judgingSet = QtCore.pyqtSignal(list,
                                    name="judgingSet",
                                    arguments=["judging"])
    _judgingCleared = QtCore.pyqtSignal(name="judgingCleared")

    def get_judging(self):
        """
        Get the currently set judging result.

        True represents a "good lift" and False "no-lift". Directions are as seen from the judges.

        :return: None or a tuple containing the results (left, middle, right)
        """

        return self._judging

    def set_judging(self, left: bool=None, middle: bool=None, right: bool=None):
        """
        Display judging results.

        True represents a "good lift", False "no-lift" and None a non existing judgement. Directions are
        from the lifter's POV.

        :param left: Judgement from the left judge
        :param middle: Judgement from the middle judge
        :param right: Judgement from the right judge
        :return: None
        """

        left = left or "NA"
        middle = middle or "NA"
        right = right or "NA"

        self._judging = (left, middle, right)
        self._judgingSet.emit(list(self._judging))

    def clear_judging(self):
        """
        Clear the currently set judging result

        :return: None
        """

        self._judging = None
        self._judgingCleared.emit()
