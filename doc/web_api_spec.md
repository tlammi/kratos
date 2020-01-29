# Web API Specification

This document covers the web API (HTTP + websocket) structure and functionality.

## HTTP

- The index page is served in `/` and provides the page used by ofiicials to manage the competitions
- Scoresheet is served in `/scoresheet` and can be used to view the current status of the competition

## Websocket

Websocket communication is used for the real time communication between the server and the client. One use
case for this is updating the judge votes asynchronically to the client. Communication is performed with JSON
formatted data. Client to server messages are denoted with *(C->S)* and server to client messages with *(S->C)*.

### Request a table (C->S)
This requests the whole table with the specified name.
```JSON
{
    "event": "getTable",
    "target": "<table name>"
}
```

### Response to Request a Table (S->C)
```JSON
{
    "event": "getTable",
    "target": "<table name>",
    "header": ["<column 1>", "<column 2>", "..."],
    "rows": [["cell00", "cell01", "..."], ["cell10", "cell11", "..."], "..." ]
}
```

### Request a new row (C->S)
This requests a new row added to the specified table with optional data added to the message. Server then
adds values to the fields that were not specified.
```JSON
{
    "event": "newRow",
    "target": "<table name>",
    "values": {
        "<column name 0>": <value 0>,
        "<column name 1>": <value 1>
    }
}

```

### New Row Added (S->C)
Sent by the server when a new row was added to a table. The message contains all of the data stored
in the row.
```JSON
{
    "event": "newRow",
    "target": "<table name>",
    "values": {
        "<column name 0>": <value 0>,
        "<column name 1>": <value 1>
    }
}
```

### Request Delete Row (C->S)
Sent by the client to request that a row were deleted.
```JSON
{
    "event": "rmRow",
    "target": "<table name>",
    "id": <number>
}
```
### Row Deleted (S->C)
Sent by the server to indicate a removal of a row.
```JSON
{
    "event": "rmRow",
    "target": "<table name>",
    "id": <number>
}
```

### Row Modification Request (C->S)
Sent by the client to request a modification of a cell.
```JSON
{
    "event": "rowModified",
    "target": "<table name>",
    "id": <number>,
    "values": {
        "column 0": "new value 0",
        "column 1": "new value 1",
        ...
    }
}
```

### Row Modified (S->C)
Sent by the server to indicate a modification of a cell.
```JSON
{
    "event": "rowModified",
    "target": "<table name>",
    "id": <number>,
    "values": {
        "column 0": "new value 0",
        "column 1": "new value 1",
        ...
    }
}
```