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
import platform
import urllib.request
import urllib.error

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
        self._wait_until_webpage("http://localhost:8080")
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

    @staticmethod
    def _wait_until_webpage(target: str, timeout_s: int = 10):
        """
        Continuously GETs the target page until no error is received

        :param target: Target URL (with http:// or similar included)
        :param timeout_s: Time after which an error is raised
        """
        LOGGER.info("Waiting for server to get up")
        start = time.time()
        while start + timeout_s > time.time():
            try:
                urllib.request.urlopen(target)
            except urllib.error.URLError:
                LOGGER.debug("Server not up")
            else:
                LOGGER.info(f"Server up after {time.time()-start}s")
                return
        raise TimeoutError(f"No response from {target} before timeout {timeout_s}")