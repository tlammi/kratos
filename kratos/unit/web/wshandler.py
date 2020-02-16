"""
Module containing functions for handling websockets.
"""
import logging
import json
import datetime
import bottle
import geventwebsocket
import sql

LOGGER = logging.getLogger(__file__)

def competitions_newrow(request: dict, client: sql.Client):  #pylint: disable=missing-function-docstring
    values = request["values"]
    if "CompetitionDate" in values:
        values["CompetitionDate"] = \
            datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
    else:
        values["CompetitionDate"] = datetime.date.today()

    client.competitions().append(**values)

    maxid = client.competitions().max_id()
    inserted_element = client.competitions()[maxid]

    request["values"] = inserted_element
    return json.dumps(request, default=str)

def competitions_rowmodified(request: dict, client: sql.Client):  #pylint: disable=missing-function-docstring
    elem_id = request["id"]
    values = request["values"]

    if "CompetitionDate" in values:
        values["CompetitionDate"] = \
            datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
    client.competitions().update(elem_id, **values)
    inserted_element = client.competitions()[elem_id]

    request["values"] = inserted_element

    responses = [json.dumps(request, default=str)]
    if "IsActive" in values:
        header, rows = client.current_competitors().to_header_and_rows()
        responses.append(json.dumps({
            "event": "tableOverwritten",
            "target": "CurrentCompetitors",
            "header": header,
            "rows": rows
        }, default=str))
    return responses


def competitions_rmrow(request: str, client: sql.Client):
    elem_id = request["id"]
    client.competitions().delete(elem_id)
    return json.dumps(request, default=str)


def competitors_newrow(request: str, client: sql.Client):  #pylint: disable=missing-function-docstring
    values = request["values"]
    if "CompetitionID" not in values:
        values["CompetitionID"] = client.competitions().where("IsActive = 1")[0]["ID"]
    client.competitors().append(**values)
    maxid = client.competitors().max_id()
    inserted_element = client.competitors()[maxid]
    inserted_element2 = client.current_competitors()[maxid]
    request["values"] = inserted_element
    resp = [
        json.dumps(request, default=str),
        json.dumps({
            "event": "newRow",
            "target": "CurrentCompetitors",
            "values": inserted_element2
        }, default=str)
    ]
    return resp


def competitors_rowmodified(request: dict, client: sql.Client):
    elem_id = request["id"]
    values = request["values"]

    client.competitors().update(elem_id, **values)
    updated_element = client.competitors()[elem_id]

    request["values"] = updated_element
    return json.dumps(request, default=str)


WEBSOCKET_HANDLERS = {
    "Competitions": {
        "newRow": competitions_newrow,
        "rowModified": competitions_rowmodified,
        "rmRow": competitions_rmrow
    },
    "Competitors": {
        "newRow": competitors_newrow,
        "rowModified": competitors_rowmodified
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
