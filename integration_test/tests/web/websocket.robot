*** Settings ***

Library  KratosLib
Library  KratosWsLib

Test Setup  Do Setup
Test Teardown  Do Teardown

Force Tags  WEBSOCKET

*** Variables ***
${URL}  ws://localhost:8080/websocket
${WS_MESSAGE_NEW_ROW}  {"event": "newRow", "target": "Competitions", "values": {"ID": 100, "Name": "A", "CompetitionDate": "2020-02-01"}}
*** Test Cases ***
Test New Row
    Connect WebSocket  url=${URL}
    Send WebSocket message   msg=${WS_MESSAGE_NEW_ROW}
    Verify WebSocket message received  match={"event": "newRow", "target": "Competitions"}

Test Remove Row
    Connect WebSocket  url=${URL}
    Send WebSocket message  msg=${WS_MESSAGE_NEW_ROW}
    Clear WebSocket receive buffer
    Send WebSocket message  msg={"event": "rmRow", "target": "Competitions", "id": 100}
    Verify WebSocket message received  match={"event": "rmRow", "target": "Competitions", "id": 100}


Test Multiple Connections
    [Tags]  FEATURE_UNDER_DEVELOPMENT
    Connect WebSocket  alias=ws1  url=${URL}
    Connect WebSocket  alias=ws2  url=${URL}

    Send WebSocket message  alias=ws1  msg=${WS_MESSAGE_NEW_ROW}
    Verify WebSocket message received  alias=ws1  match={"event": "newRow", "target": "Competitions"}
    Verify WebSocket message received  alias=ws2  match={"event": "newRow", "target": "Competitions"}

*** Keywords ***
Do Setup
    Start kratos web server

Do Teardown
    Kill all kratos processes
    Disconnect all WebSockets
