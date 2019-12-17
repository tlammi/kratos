import pytest

from util import mqtt_match


@pytest.mark.parametrize("filter,topic", [
    ("#", "/hello/world"),
    ("#", "hello/world"),
    ("/hello/world", "/hello/world"),
    ("+", "hello"),
    ("/+", "/hello")
])
def test_mqtt_match_match(filter, topic):
    assert mqtt_match(filter, topic)


@pytest.mark.parametrize("filter,topic", [
    ("#", "$SYS"),
    ("/#", "$SYS"),
    ("/+/a/#", "/hello/b/world")
])
def test_mqtt_match_no_match(filter, topic):
    assert not mqtt_match(filter, topic)


@pytest.mark.parametrize("filter", [
    "#/",
    "/hello/#/world"
])
def test_mqtt_match_invalid_filter(filter):
    with pytest.raises(ValueError):
        mqtt_match(filter, "/hello/world")
