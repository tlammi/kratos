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

def handle_new_row(target: str, values: dict, client: sql.Client):
    """
    Handle new row event

    :param target: Target table name
    :param values: Dict of values to insert. Non-specified values will be set to defaults
    :param client: SQL client used for accessing the database
    :return: Response string
    """
    if(target == "competitions"):
        if "CompetitionDate" in values:
            values["CompetitionDate"] = datetime.datetime.strptime(values["CompetitionDate"], "%Y-%m-%d")
        else:
            values["CompetitionDate"] = datetime.date.today()
        client.competitions().append(**values)

        maxid = client.competitions().max_id()

        inserted_element = client.competitions()[maxid]
        # datetime.date does not serialize, but str does
        inserted_element["CompetitionDate"] = str(inserted_element["CompetitionDate"])
        return json.dumps(
            {"event": "newRow", "target": "competitions", "values": inserted_element})
    else:
        raise ValueError("Non-supported target table %s", target)

def handle_get_table(target: str, client: sql.Client):
    """
    Handling function for getTable event

    :param target: Target table
    :param client: SQL client
    :return: Response string
    """
    if(target == "competitions"):
        header, rows = client.competitions().to_header_and_rows()
        resp = {}
        resp["event"] = "getTable"
        resp["target"] = "competitions"
        resp["header"] = header
        for index, row in enumerate(rows):
            for key, val in enumerate(row):
                if isinstance(val, datetime.date):
                    rows[index][key] = str(val)
        resp["rows"] = rows
        print(f"resp: {resp}")
        return json.dumps(resp)

def handle_update_row(target: str, id: int, values: dict, client: sql.Client):
    """
    Handling function for row update

    :param target: Target table
    :param id: ID of the element to target
    :param values: Dict of values to insert. Non-specified values will be left unmodified
    :param client: SQL client
    """
    if target == "competitions":
        tmp = values.copy()
        if "CompetitionDate" in tmp:
            tmp["CompetitionDate"] = datetime.datetime.strptime(tmp["CompetitionDate"], "%Y-%m-%d")
        client.competitions().update(id, **tmp)

    return json.dumps({"event": "rowModified", "target": "competitions", "id": id, "values": values})

def handle_rm_row(target: str, id: int, client: sql.Client):
    """
    Handling function for removing a table entry

    :param target: Target table
    :param id: ID to remove
    :param client: SQL client
    """
    if target == "competitions":
        client.competitions().delete(id)
        return json.dumps({"event": "rmRow", "target": "competitions", "id": id})

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
                print(f"raw reguest: {raw_reguest}")
                if raw_reguest is None:
                    continue
                json_request = json.loads(raw_reguest)
            except json.decoder.JSONDecodeError:
                LOGGER.error("Non-JSON string received: %s", raw_reguest)
            else:
                if json_request["event"] == "newRow":
                    wsock.send(handle_new_row(json_request["target"],
                               json_request["values"], client))
                elif json_request["event"] == "getTable":
                    wsock.send(handle_get_table(json_request["target"], client))
                elif json_request["event"] == "rowModified":
                    wsock.send(handle_update_row(json_request["target"],
                                                 json_request["id"],
                                                 json_request["values"],
                                                 client))
                elif json_request["event"] == "rmRow":
                    wsock.send(handle_rm_row(json_request["target"], json_request["id"], client))

        except geventwebsocket.WebSocketError:
            break
