"""
Module containing functions for handling websockets.
"""
import logging
import json
import datetime
import bottle
import copy
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
    return [request]

def competitions_rowmodified(request: dict, client: sql.Client):  #pylint: disable=missing-function-docstring
    elem_id = request["id"]
    values = request["values"]

    if "CompetitionDate" in values:
        values["CompetitionDate"] = \
            datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
    client.competitions().update(elem_id, **values)
    inserted_element = client.competitions()[elem_id]

    request["values"] = inserted_element

    responses = [request]
    if "IsActive" in values:
        header, rows = client.current_competitors().to_header_and_rows()
        responses.append({
            "event": "tableOverwritten",
            "target": "CurrentCompetitors",
            "header": header,
            "rows": rows
        })
    return responses


def competitions_rmrow(request: str, client: sql.Client):
    elem_id = request["id"]
    response = [request.copy()]
    if client.competitions()[elem_id]["IsActive"]:
        client.competitions()[elem_id].update(IsActive=False)
        h, r = client.current_competitors().to_header_and_rows()
        response.append(
            {
                "event": "tableOverwritten",
                "target": "CurrentCompetitors",
                "header": h,
                "rows": r
            }
        )
    client.competitions().delete(elem_id)
    return response


def competitors_newrow(request: str, client: sql.Client):  #pylint: disable=missing-function-docstring
    values = request["values"]
    if "CompetitionID" not in values:
        values["CompetitionID"] = client.competitions().where("IsActive = 1")[0]["ID"]

    client.competitors().append(**values)
    maxid = client.competitors().max_id()
    competition_id = client.competitors()[maxid]["CompetitionID"]
    resp =  [
        {
            "event": "newRow",
            "target": "Competitors",
            "values": client.competitors()[maxid]
        }
    ]
    if client.competitions()[competition_id]["IsActive"]:
        resp.append({
            "event": "newRow",
            "target": "CurrentCompetitors",
            "values": client.current_competitors()[maxid]
        })
    return resp


def competitors_rowmodified(request: dict, client: sql.Client):
    elem_id = request["id"]
    values = request["values"]

    client.competitors().update(elem_id, **values)
    updated_element = client.competitors()[elem_id]
    request["values"] = updated_element
    resp = [request]
    competition_id = client.competitors()[elem_id]["CompetitionID"]

    if client.competitions()[competition_id]["IsActive"]:
        resp.append(
            {
                "event": "rowModified",
                "target": "CurrentCompetitors",
                "id": elem_id,
                "values": client.current_competitors()[elem_id]
            }
        )

    return resp

def competitors_rmrow(request: dict, client: sql.Client):
    elem_id = request["id"]
    competition_id = client.competitors()[elem_id]["CompetitionID"]
    response = [request]
    if client.competitions()[competition_id]["IsActive"]:
        tmp = copy.deepcopy(request)
        tmp["target"] = "CurrentCompetitors"
        response.append(
            tmp
        )
    client.competitors().delete(elem_id)
    return response

WEBSOCKET_HANDLERS = {
    "Competitions": {
        "newRow": competitions_newrow,
        "rowModified": competitions_rowmodified,
        "rmRow": competitions_rmrow
    },
    "Competitors": {
        "newRow": competitors_newrow,
        "rowModified": competitors_rowmodified,
        "rmRow": competitors_rmrow
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
                    for r in resp:
                        wsock.send(json.dumps(r, default=str))
                except KeyError:
                    LOGGER.error("Unkown target %s or event %s", target, event)
                    raise

        except geventwebsocket.WebSocketError:
            break
