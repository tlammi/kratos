"""
The base class for creating more complex GUI screens
"""

import os

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtQuick as QtQuick


class Screen:
    """
    Base screen class that creates an Qt application with argument passing and QML
    resource loading
    """

    # pylint: disable=too-few-public-methods
    # This is a base class and has (at the moment) only limited functionality

    def __init__(self, argv=None):
        """
        Ctor

        :param argv: Arguments passed to the underlying QGuiApplication
        """

        argv = argv or []

        # QGuiApplication usually takes sys.argv parameters as input so the first
        # argument is ignored
        self._app = QtGui.QGuiApplication([""] + argv)
        self._view = QtQuick.QQuickView()
        self._view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

    def run(self):
        """
        Display the screen

        Makes the QML view visible and start the Qt event loop. This call blocks
        until the application window is closed.

        :return: The return value from the Qt application
        """

        self._view.show()
        return self._app.exec()

    def _load(self, file_name):
        qml_path = os.path.join(os.path.dirname(__file__), file_name)
        self._view.setSource(QtCore.QUrl.fromLocalFile(os.path.abspath(qml_path)))

        if self._view.status() == QtQuick.QQuickView.Error:
            raise RuntimeError(f"Failed to load QML resource '{qml_path}'" +
                               f" with {len(self._view.errors())} errors")
