"""
An example module
"""

import logging

LOGGER = logging.getLogger(__name__)


class Example:
    """
    Example class
    """

    def __init__(self):
        LOGGER.info("This is an example")

    @staticmethod
    def method1():
        """
        Method 1
        """
        LOGGER.info("method1")

    @staticmethod
    def method2():
        """
        Method 2
        """
        LOGGER.info("method2")
