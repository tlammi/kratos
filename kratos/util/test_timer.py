import pytest
import time

from util import Timer


def test_init():
    t = Timer()
    assert t.running == False
    assert t.remaining_time == 0

def test_invalid_start():
    t = Timer()

    with pytest.raises(ValueError, match="No timeout value stored, please provide one"):
        t.start()

    assert t.running == False
    assert t.remaining_time == 0
    
    with pytest.raises(ValueError, match="Invalid timeout value: 0"):
        t.start(timeout=0.9)

    assert t.running == False
    assert t.remaining_time == 0

def test_multiple_starts():
    t = Timer()

    t.start(timeout=2)

    assert t.running == True
    
    with pytest.raises(RuntimeError, match="Timer is already running"):
        t.start()

    assert t.running == True
    time.sleep(0.1)

    t.stop()

def test_invalid_stop():
    t = Timer()
    
    t.stop()

    assert t.running == False
    assert t.remaining_time == 0


def test_multiple_stops():
    t = Timer()

    t.start(timeout=2)

    time.sleep(0.1)

    t.stop()

    status = t.running
    remaining = t.remaining_time

    assert status == False
    assert remaining > 0

    t.stop()

    assert t.running == status
    assert t.remaining_time == remaining

def test_start_after_stop():
    t = Timer()

    t.start(timeout=2)

    time.sleep(0.1)

    t.stop()

    t.start()

    assert t.running == True
    assert t.remaining_time > 0

    time.sleep(0.1)

    t.stop()

def test_clearing():
    t = Timer()

    t.start(timeout=2)
    time.sleep(0.1)
    t.stop()

    t.clear()

    assert t.running == False
    assert t.remaining_time == 0

    with pytest.raises(ValueError, match="No timeout value stored, please provide one"):
        t.start()

    t.start(timeout=2)
    time.sleep(0.1)
    t.stop()

def test_remaining_time():
    t = Timer()

    t.start(timeout=1)
    time.sleep(0.1)
    t.stop()

    assert t.remaining_time == 0