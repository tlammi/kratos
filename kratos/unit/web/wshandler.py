"""
Module containing functions for handling websockets.
"""
import logging
import json
import datetime
import bottle
import geventwebsocket
import sql
import util

LOGGER = logging.getLogger(__file__)

def competitions_newrow(request: dict, client: sql.Client):
    values = request["values"]
    if "CompetitionDate" in values:
        values["CompetitionDate"] = datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
    else:
        values["CompetitionDate"] = datetime.date.today()

    client.competitions().append(**values)

    maxid = client.competitions().max_id()
    inserted_element = client.competitions()[maxid]

    request["values"] = inserted_element
    return util.serialize_dict(request)


def competitions_gettable(request: dict, client: sql.Client):
    header, rows = client.competitions().to_header_and_rows()
    resp = request
    resp["header"] = header
    for index, row in enumerate(rows):
        for key, val in enumerate(row):
            if isinstance(val, datetime.date):
                rows[index][key] = str(val)
    resp["rows"] = rows
    LOGGER.debug("resp: %s", resp)
    return util.serialize_dict(resp)

def competitions_rowmodified(request: dict, client: sql.Client):
    elem_id = request["id"]
    values = request["values"]

    if "CompetitionDate" in values:
        values["CompetitionDate"] = datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
    client.competitions().update(elem_id, **values)
    inserted_element = client.competitions()[elem_id]

    request["values"] = inserted_element

    responses = [util.serialize_dict(request)]
    if "IsActive" in values:
        responses.append(current_competitors_gettable({
            "event": "getTable",
            "target": "CurrentCompetitors"
        }, client))
    return responses

def competitions_rmrow(request: str, client: sql.Client):
    elem_id = request["id"]
    client.competitions().delete(elem_id)
    return util.serialize_dict(request)

def competitors_newrow(request: str, client: sql.Client):
    values = request["values"]
    if "CompetitionID" not in values:
        values["CompetitionID"] = client.competitions().where("IsActive = 1")[0]["ID"]
    client.competitors().append(**values)
    maxid = client.competitors().max_id()
    inserted_element = client.competitors()[maxid]
    inserted_element2 = client.current_competitors()[maxid]
    request["values"] = inserted_element
    resp = [
        util.serialize_dict(request),
        util.serialize_dict({
            "event": "newRow",
            "target": "CurrentCompetitors",
            "values": inserted_element2
        })
    ]

    return resp

def competitors_gettable(request: dict, client: sql.Client):
    header, rows = client.competitors().to_header_and_rows()
    resp = request
    resp["header"] = header
    for index, row in enumerate(rows):
        for key, val in enumerate(row):
            if isinstance(val, datetime.date):
                rows[index][key] = str(val)
    resp["rows"] = rows
    LOGGER.debug("resp: %s", resp)
    return json.dumps(resp)

def competitors_rowmodified(request: dict, client: sql.Client):
    elem_id = request["id"]
    values = request["values"]

    client.competitors().update(elem_id, **values)
    updated_element = client.competitors()[elem_id]

    request["values"] = updated_element
    return util.serialize_dict(request)

def current_competitors_gettable(request: dict, client: sql.Client):
    header, rows = client.current_competitors().to_header_and_rows()
    resp = request
    resp["header"] = header
    resp["rows"] = rows
    LOGGER.debug("resp: %s", resp)
    return util.serialize_dict(resp)

WEBSOCKET_HANDLERS = {
    "Competitions": {
        "newRow": competitions_newrow,
        "getTable": competitions_gettable,
        "rowModified": competitions_rowmodified,
        "rmRow": competitions_rmrow
    },
    "Competitors": {
        "newRow": competitors_newrow,
        "getTable": competitors_gettable,
        "rowModified": competitors_rowmodified
    },
    "CurrentCompetitors": {
        "getTable": current_competitors_gettable
    }
}

def serve_websocket(client: sql.Client):
    """
    Main function for serving websockets

    :param client: SQL client
    """
    wsock = bottle.request.environ.get("wsgi.websocket")
    if not wsock:
        bottle.abort(400, "Expected WebSocket request.")
    while True:
        try:
            try:
                raw_reguest = wsock.receive()
                LOGGER.info("Raw request received: %s", raw_reguest)
                if raw_reguest is None:
                    continue
                json_request = json.loads(raw_reguest)
            except json.decoder.JSONDecodeError:
                LOGGER.error("Non-JSON string received: %s", raw_reguest)
            else:

                target = json_request["target"]
                event = json_request["event"]
                try:
                    resp = WEBSOCKET_HANDLERS[target][event](json_request, client)
                    LOGGER.info("Sending response: %s", resp)
                    if not isinstance(resp, (list, tuple)):
                        resp = [resp]
                    for r in resp:
                        wsock.send(r)
                except KeyError:
                    LOGGER.error("Unkown target %s or event %s", target, event)
                    raise

        except geventwebsocket.WebSocketError:
            break
