"""
Main file and entrypoint for web unit
"""
import argparse
import os
import datetime
import logging
import json
import bottle
import gevent.monkey
import gevent.pywsgi
import geventwebsocket

import sql
from . import wshandler


THISDIR = os.path.dirname(os.path.realpath(__file__))
HTML_DIR = os.path.join(THISDIR, "html")
HTML_FILE = os.path.join(HTML_DIR, "index.html")


LIFTER_TABLE_HEADERS = ["Last Name", "First Names", "Body Weight",
                        "Snatch 1", "Snatch 2", "Snatch 3",
                        "C&J 1", "C&J 2", "C&J 3",
                        "Tot", "Sinclair"]

LOGGER = logging.getLogger(__file__)

def serve_index():
    """
    Callback for serving website index

    :return: HTML
    """
    with open(HTML_FILE, "r") as f:
        data = f.read()

    return data

def serve_favicon():
    """
    Callback for serving favicon
    """
    return bottle.static_file("favicon.ico", root=os.path.join(THISDIR, "favicon"))

def serve_css(filename):
    """
    Serves files placed in css/ directory

    :param filename: File in css/
    :return: String read from the file
    """
    LOGGER.debug("serving %s", filename)
    return bottle.static_file(filename, root=os.path.join(THISDIR, "css"))

def serve_script(filename):
    """
    Serves files placed in script/ directory

    :param filename: File in script/
    :return String read fromt the file
    """
    return bottle.static_file(filename,
                              root=os.path.join(THISDIR, "script"))


def serve_tables(tablename: str, client: sql.Client):
    """
    Serves tables present in paths /tables/<tablename>

    :param tablename: Requested tables
    :param client: Client used for accessing SQL database.
        Initialized before the function execution.
    :return: Table as HTML string
    """
    LOGGER.debug("serving %s", tablename)
    if tablename == "Competitions":
        header, rows = client.competitions().to_header_and_rows()
    elif tablename == "Competitors":
        header, rows = client.competitors().to_header_and_rows()
    elif tablename == "CurrentCompetitors":
        header, rows = client.current_competitors().to_header_and_rows()
    else:
        bottle.abort(400, f"Unknown table '{tablename}'")
    resp = {}
    resp["header"] = header
    resp["rows"] = rows
    LOGGER.debug("resp: %s", resp)
    return json.dumps(resp, default=str)

def add_cli_args(_parser: argparse.ArgumentParser):
    """
    Add CLI args

    :param _parser: CLI arg parser
    :return: The modified parser
    """


def run(_args: argparse.Namespace):
    """
    Execute webserver

    :param _args: Parsed CLI args
    :return: None
    """
    client = sql.Client("sqlite:///:memory:")
    client.competitions().append(Name="Kevät ranking 2020",
                                 CompetitionDate=datetime.date(2020, 3, 3),
                                 IsActive=False)
    client.competitions().append(Name="Syys ranking 2020",
                                 CompetitionDate=datetime.date(2020, 9, 3),
                                 IsActive=False)
    bottle.get(r"/css/<filename>")(serve_css)
    bottle.get("/")(serve_index)
    bottle.get("/favicon.ico")(serve_favicon)
    bottle.get(r"/tables/<tablename>")(lambda tablename: serve_tables(tablename, client))
    bottle.get(r"/script/<filename>")(serve_script)
    bottle.get(r"/websocket")(lambda: wshandler.serve_websocket(client))

    gevent.monkey.patch_all()  # Magic
    bottle.run(server="gevent", host="localhost", port=8080,
               debug=True, handler_class=geventwebsocket.handler.WebSocketHandler)
