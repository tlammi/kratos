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


def xml_wrap(tag: str, text: str, attrs: list = None):
    """
    Generate xml tag strings

    :param tag: Tag name
    :param text: Text inside the element
    :param attrs: XML attributes
    :return: Generated string
    """
    attrs = attrs or []
    attrstr = " ".join(attrs)
    if text:
       return f"<{tag} {attrstr}>{text}</{tag}>"
    return f"<{tag} {attrstr}/>"


def to_html_table(header: list, values: list):
    """
    Converts header and values to html table presentation

    :param header: Header row
    :param values: List of lists (or similar) containing the data
    :return: HTML table as string
    """
    headerstr = "".join([xml_wrap("th", i) for i in header])
    headerstr = xml_wrap("tr", headerstr)
    headerstr = xml_wrap("thead", headerstr)

    datastr = ""
    for row in values:
        tmp = "".join([xml_wrap("td", elem) for elem in row])
        tmp = xml_wrap("tr", tmp)
        datastr += tmp

    datastr = xml_wrap("tbody", datastr)

    return xml_wrap("table", headerstr+datastr)

