"""
Oneshot timer that can be stopped with max latency of 100 ms.
"""
import concurrent.futures as futures
import datetime
import threading
import time
import typing


class Timer:
    def __init__(self):
        self._running = threading.Event()
        self._remaining_time = 0

        self._worker_thread = None

    def clear(self):
        """
        Clear the timer remaining seconds.
        """

        if self._running.is_set():
            raise RuntimeError("Timer is running")
        self._remaining_time = 0

    def start(self, timeout: int=None,
              once_per_second: typing.Callable[[int], None]=None,
              expired: typing.Callable[[], None]=None) -> None:
        """
        Start the timer.

        This call can return before the timer has started and care should be taken
        to not stop the timer immediately after starting as this can cause a
        deadlock.

        :param timeout: timeout in seconds (will be rounded to whole seconds)
        :param once_per_second: this callback ei called once per second on the
                                second with the remaining time in seconds as the
                                parameter
        :param expired: this callback is called once the timer has expired
        """

        if self._running.is_set():
            raise RuntimeError("Timer is already running")

        if timeout == None and self._remaining_time == 0:
            raise ValueError("No timeout value stored, please provide one")

        timeout = int(timeout) if timeout else self._remaining_time
        if timeout < 1:
            raise ValueError(f"Invalid timeout value: {timeout}")

        self._timeout = timeout
        self._once_per_second_cb = once_per_second
        self._expired_cb = expired
        self._worker_thread = threading.Thread(target=self._worker)
        self._worker_thread.start()
        self._running.set()
    
    def stop(self) -> int:
        """
        Stop the running timer. If there is around 100 ms left in the
        timer there is no quarantee that the timer will be stopped
        before the it expires.

        Care should be taken to not stop the timer immediately after
        starting as this can cause a deadlock.

        :return: The remaining time as whole seconds (rounded down) when
                 the timer was stopped
        """

        self._running.clear()
        if self._worker_thread:
            self._worker_thread.join()

        return self._remaining_time
    
    @property
    def remaining_time(self):
        """
        :return: the remaining time in time as whole seconds (rounded down)
        """

        return self._remaining_time
    
    @property
    def running(self):
        """
        :return: True if the timer is running, otherwise False
        """

        return self._running.is_set()
    
    def _worker(self) -> int:
        cb_executor = futures.ThreadPoolExecutor()

        now = datetime.datetime.now
        one_tick = datetime.timedelta(milliseconds=100)
        ticks_per_second = datetime.timedelta(seconds=1) // one_tick

        timeout = self._timeout * ticks_per_second

        self._running.wait()

        target = now()

        for remaining_ticks in range(timeout, 0, -1):
            if not self._running.is_set():
                break
            else:
                target += one_tick
                time.sleep((target - now()).total_seconds())

                if remaining_ticks % ticks_per_second == 0:
                    self._remaining_time = remaining_ticks // ticks_per_second
                    if self._once_per_second_cb:
                        cb_executor.submit(self._once_per_second_cb,
                                           self._remaining_time)

        remaining_ticks -= 1
        self._remaining_time = remaining_ticks // ticks_per_second

        if remaining_ticks == 0:
            if self._expired_cb:
                cb_executor.submit(self._expired_cb)