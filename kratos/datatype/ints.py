"""
Sized int type definitions
"""
# pylint: disable=missing-class-docstring

import abc


class SizedInt(abc.ABC):
    """
    Abstract base class for integers with known byte sizes
    """

    @abc.abstractmethod
    def __int__(self):
        pass

    @abc.abstractmethod
    def __len__(self):
        pass

    @abc.abstractmethod
    def __add__(self, other):
        pass

    @abc.abstractmethod
    def __sub__(self, other):
        pass

    @abc.abstractmethod
    def __mul__(self, other):
        pass

    @abc.abstractmethod
    def __mod__(self, other):
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    @abc.abstractmethod
    def __lt__(self, other):
        pass

    @abc.abstractmethod
    def __gt__(self, other):
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        pass

    @abc.abstractmethod
    def __le__(self, other):
        pass

    @abc.abstractmethod
    def __ge__(self, other):
        pass

    @abc.abstractclassmethod
    def from_bytes(cls, bytes_in, endianness="big"):
        pass

    @abc.abstractmethod
    def to_bytes(self, endianness="big"):
        pass


def _intclass(bcount, signed):
    class IntImpl(SizedInt):
        """
        Helper class used for constructing sized integers
        """
        _bcount = bcount
        _signed = signed

        def __init__(self, val: int):

            self._val = val

            # This checks that the value fits the ranges
            self.to_bytes()

        def __int__(self):
            return self._val

        def __str__(self):
            return str(self._val)

        def __repr__(self):
            return "%s(%s)" % (self.__class__.__name__, self._val)

        def __len__(self):
            return self._bcount

        def __add__(self, other):
            return self.__class__(self._val + int(other))

        def __sub__(self, other):
            return self.__class__(self._val - int(other))

        def __mul__(self, other):
            return self.__class__(self._val * int(other))

        def __mod__(self, other):
            return self.__class__(self._val % int(other))

        def __eq__(self, other):
            return self._val == int(other)

        def __lt__(self, other):
            return self._val < int(other)

        def __gt__(self, other):
            return self._val > int(other)

        def __ne__(self, other):
            return self._val != int(other)

        def __le__(self, other):
            return self._val <= int(other)

        def __ge__(self, other):
            return self._val >= int(other)

        @classmethod
        def from_bytes(cls, bytes_in, endianness="big"):
            """
            Converts bytes to a class instance

            :param bytes_in: Iterable of values between 0 and 255.
                Extra bytes are ignored if more bytes are passed than required.
            :param endianness: Endianness used for conversion.
            :return: Sized integer object
            """
            bytes_in = bytes_in[:cls._bcount]
            return cls(int.from_bytes(bytes_in, endianness, signed=cls._signed))

        def to_bytes(self, endianness="big"):
            """
            Converts class instance to bytes

            :param endianness: Endianness used for conversion
            :return: bytes-object constructed from a sized integer object
            """
            return self._val.to_bytes(self._bcount, endianness, signed=self._signed)

    return IntImpl


class Int8(_intclass(1, True)):
    pass


class Int16(_intclass(2, True)):
    pass


class Int32(_intclass(4, True)):
    pass


class Int64(_intclass(8, True)):
    pass


class Uint8(_intclass(1, False)):
    pass


class Uint16(_intclass(2, False)):
    pass


class Uint32(_intclass(4, False)):
    pass


class Uint64(_intclass(8, False)):
    pass
