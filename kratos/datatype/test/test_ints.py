
from datatype.ints import *
import sys
import pytest
import itertools

CLASS_LIST = [
    Uint8,
    Uint16,
    Uint32,
    Uint64,

    Int8,
    Int16,
    Int32,
    Int64
]

IS_SIGNED_LIST = [False] * 4 + [True] * 4
BYTE_COUNT_LIST = [1, 2, 4, 8]*2

MIN_VAL_LIST = [0]*4 + [-2**(i*8-1) for i in [1, 2, 4, 8]]
MAX_VAL_LIST = [2**(i*8)-1 for i in [1, 2, 4, 8]] + \
    [2**(i*8-1)-1 for i in [1, 2, 4, 8]]


def test_sizes():
    for c, b in zip(CLASS_LIST, BYTE_COUNT_LIST):
        assert c._bcount == b
        assert len(c(0)) == b


def test_signed():
    for c, s in zip(CLASS_LIST, IS_SIGNED_LIST):
        assert c._signed == s


def test_min():
    for c, m in zip(CLASS_LIST, MIN_VAL_LIST):
        _ = c(m)
        with pytest.raises(OverflowError):
            _ = c(m-1)


def test_max():
    for c, m in zip(CLASS_LIST, MAX_VAL_LIST):
        _ = c(m)
        with pytest.raises(OverflowError):
            _ = c(m + 1)


def test_sum():
    a = Uint16(100)
    b = Int32(-101)
    assert b + a == -1
    a += 1
    assert isinstance(a, Uint16)
    assert isinstance(b + a, Int32)


def test_sum_all_types():

    for a, b in itertools.combinations(CLASS_LIST, 2):
        res = a(1) + b(2)
        assert res == 3
        assert type(res) == a


def test_sub():
    a = Uint16(4)
    b = Int64(100)

    assert b - a == 96
    b -= 99

    assert b == 1
    assert isinstance(b, Int64)


def test_sub_all_types():
    for a, b in itertools.combinations(CLASS_LIST, 2):
        res = a(3) - b(1)
        assert res == 2
        assert type(res) == a


def test_mul():
    a = Uint8(4)
    b = Uint16(100)

    b *= a

    assert b == 400

    assert isinstance(b, Uint16)


def test_mul_all_types():
    for a, b in itertools.combinations(CLASS_LIST, 2):
        res = a(3) * b(2)
        assert res == 6
        assert type(res) == a


def test_mod():
    a = Uint64(3)
    b = Int8(101)
    assert b % a == 2
    assert isinstance(b, Int8)


def test_mod_all_types():
    for a, b in itertools.combinations(CLASS_LIST, 2):
        res = a(7) % b(3)
        assert res == 1
        assert type(res) == a


def test_comparison():
    assert Uint8(8) == Int64(8)
    assert Uint8(7) == Uint8(7)

    assert Uint8(100) < Uint64(101)
    assert Uint8(100) > Uint64(99)
    assert Uint8(100) <= Int8(100)
    assert Uint8(100) <= Int8(101)
    assert Uint8(100) >= Int8(100)
    assert Uint8(100) >= Int8(99)
