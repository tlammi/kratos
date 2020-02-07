"""
Library for managing kratos
"""

import os
import sys
import signal
import logging
import atexit
import subprocess
import time

LOGGER = logging.getLogger(__file__)


class KratosLib:
    """
    Library for managing kratos
    """

    def __init__(self):
        self._processes = []
        # Make sure that the subprocesses are killed
        atexit.register(self.kill_all_kratos_processes)

    def start_kratos_web_server(self, *args, **kwargs):
        """
        Starts the web server functionality of kratos

        :param args: Currently ignored
        :param kwargs: Currently ignored
        """
        LOGGER.info("Starting kratos webserver")
        self._processes.append(subprocess.Popen([sys.executable, "-m" "kratos", "webserver"]))
        LOGGER.info("kratos webserver started")

    def kill_all_kratos_processes(self):
        """
        Kills all processes started via the library
        """
        for i, p in enumerate(self._processes):
            if p is not None:
                pid = p.pid
                os.kill(pid, signal.SIGINT)
                self._processes[i] = None
        self._processes = [p for p in self._processes if p is not None]
