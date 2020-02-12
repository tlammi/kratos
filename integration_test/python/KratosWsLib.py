"""
WebSocket library specific for kratos
"""
import json
import threading
import time
import logging
import queue
import asyncio
from typing import Union

import websockets
import websockets.client


LOGGER = logging.getLogger(__file__)


class _WsImpl:
    """
    Implementing class for a WebSocket connection
    """

    _TIMEOUT_S = 10.0

    def __init__(self, url: str):
        """
        Creates a connection and connects

        :param url: URL to connect to
        """
        self._event_loop, self._thread = self._create_and_start_event_thread()
        self._conn = self._perform_connect(self._event_loop, url)
        self._receiver_task = asyncio.run_coroutine_threadsafe(self._receiver(self._conn),
                                                               self._event_loop)
        self._msg_buffer = []
        self._queue = queue.Queue()

    def __del__(self):
        """
        Deletes object and closes the connection
        """
        self._receiver_task.cancel()
        self._event_loop.stop()
        self._queue = None

    def msg_buffer(self):
        """
        Access receive buffer of the connection

        :return: List of received messages in the buffer
        """
        while not self._queue.empty():
            self._msg_buffer.append(self._queue.get_nowait())
        return self._msg_buffer

    def clear_buffer(self):
        """
        Clears the message buffer
        """
        self._msg_buffer = []

    def send(self, msg: str):
        """
        Sends a WebSocket message
        :param msg: Message to send as string
        """
        handle = asyncio.run_coroutine_threadsafe(
            self._send(self._conn, msg), self._event_loop)
        handle.result()

    @staticmethod
    def _create_and_start_event_thread():
        """
        Starts a new thread and an asyncio event loop in it

        :return: event_loop, thread
        """
        event_loop = asyncio.new_event_loop()
        thread = threading.Thread(target=event_loop.run_forever, daemon=True)
        thread.start()
        return event_loop, thread

    def _perform_connect(self, event_loop, url: str):
        """
        Calls connect coroutine

        :param event_loop: Event loop to run the coroutine in
        :param url: URL to connect to
        :return: websockets.WebSocketClientProtocol
        """
        return asyncio.run_coroutine_threadsafe(self._connect(url), event_loop).result()

    @staticmethod
    async def _connect(url: str):
        conn = await websockets.client.connect(url)
        return conn

    @staticmethod
    async def _send(conn: websockets.WebSocketClientProtocol, msg: str):
        await conn.send(msg)

    async def _receiver(self, conn: websockets.WebSocketClientProtocol):
        while True:
            msg = await conn.recv()
            self._queue.put(msg)


class KratosWsLib:
    """
    Public interface of the WebSocket Robot Framework library
    """

    def __init__(self):
        self._conns = {}

    def connect_websocket(self, alias: str = None, url: str = None):
        """
        Creates a WebSocket connection

        :param alias: Alias of the connection, None is a valid alias
        :param url: URL to connect to
        """
        if not url:
            raise ValueError("URL not specified")
        LOGGER.info("Creating a new WebSocket connection to %s with alias %s", url, alias)
        self._conns[alias] = _WsImpl(url)
        LOGGER.info("Connection established")

    def disconnect_websocket(self, alias: str = None):
        """
        Disconnects a previously connected WebSocket connection

        :param alias: Alias of the connection to disconnect
        """
        if alias not in self._conns:
            LOGGER.info("Connection with alias %s not connected")
            return
        LOGGER.info("Closing WebSocket connection")
        del self._conns[alias]
        LOGGER.info("Connection closed")

    def disconnect_all_websockets(self):
        """
        Disconnects all WebSocket connections established via the interface

        """
        keys = list(self._conns.keys())
        for k in keys:
            del self._conns[k]

    def send_websocket_message(self, alias: str = None, msg: Union[str, dict] = None):
        """
        Sends a WebSocket message via the connection with given alias

        :param alias: Alias of the connection
        :param msg: Message to send
        """
        msg = msg if isinstance(msg, str) else json.dumps(msg)
        self._conns[alias].send(msg)

    def verify_websocket_message_received(self,
                                          alias: str = None,
                                          match: Union[str, dict] = None,
                                          timeout_s: float = 10.0):
        """
        Check that a matching WebSocket message is received via the given connection

        :param alias: Alias of the connection to use
        :param match: Filter to match against. Filter matches a message if all
            keys of filter are present in the message and each value corresponding
            to a key is equal in message and filter.
        :param timeout_s: Timeout to wait for messages in seconds
        """
        match = match if isinstance(match, dict) else json.loads(match)
        start = time.time()
        while True:
            for msg in self._conns[alias].msg_buffer():
                msg = json.loads(msg)
                if all([k in msg and msg[k] == v for k, v in match.items()]):
                    return
            time.sleep(1)
            if time.time() > start + timeout_s:
                break
        raise ValueError(f"No messages matching to {match} "
                         f"found from connection with alias {alias}")

    def matching_websocket_messages_received(self,
                                             alias: str = None,
                                             match: Union[str, dict] = None):
        """
        Returns the number of matching messages in the receive buffer

        :param alias: Alias of the connection to use
        :param match: Filter to match against, see verify_websocket_message_received for details
        :return: Number of matching messages
        """
        if match is None:
            match = {}
        elif isinstance(match, str):
            match = json.loads(match)

        counter = 0
        for msg in self._conns[alias].msg_buffer():
            msg = json.loads(msg)
            if all([k in msg and msg[k] == v for k, v in match.items()]):
                counter += 1
        return counter

    def clear_websocket_receive_buffer(self, alias: str = None):
        """
        Clears the receive buffer of the specified connection

        :param alias: Alias of the connection for which the buffer is cleared
        """
        self._conns[alias].clear_buffer()
