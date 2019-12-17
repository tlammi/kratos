"""
Utility functions
"""


def mqtt_match(topic_filter: str, topic: str):
    """
    Checks if the topic filter and topic match

    :param topic_filter: Topic filter to match
    :param topic: Topic to match agains topic filter
    :return: True, if the filter and the topic match, else False
    """
    topic_filter = topic_filter.split("/")

    if "#" in topic_filter and topic_filter[-1] != "#":
        raise ValueError("Invalid topic filter %s" % "/".join(topic_filter))

    topic = topic.split("/")

    for f, t in zip(topic_filter, topic):
        if f == "#" and not t.startswith("$"):
            return True
        if f == "+":
            pass
        elif f == t:
            pass
        else:
            return False

    return True
