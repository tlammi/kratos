import pytest
import datetime
import json
import copy
import sql
from unit.web.wshandler import *

client = sql.Client("sqlite:///:memory:")

@pytest.fixture
def setup_and_teardown():
    client.competitions().append(Name="Active", CompetitionDate=datetime.date(2020,2,2), IsActive=True)
    client.competitions().append(Name="NotActive", CompetitionDate=datetime.date(2020,3,4))
    client.competitors().append(FirstNames="FirstNamesA", LastName="LastNameA", CompetitionID=1)
    client.competitors().append(FirstNames="FirstNamesB", LastName="LastNameB", CompetitionID=2)
    yield
    client.competitions().delete_all()
    client.competitors().delete_all()

def match_dicts(dict_in: dict, filter: dict):
    try:
        for key, value in filter.items():
            if isinstance(value, dict):
                if not match_dicts(dict_in[key], value):
                    return False
            elif dict_in[key] != value:
                return False
    except KeyError:
        return False
    return True


@pytest.mark.parametrize("function, target, values, expected_resp_count, expected_response_filters",[
    (
        competitions_newrow,
        "Competitions",
        {"Name": "C", "CompetitionDate": "2020-02-02"},
        1,
        [
            {"event": "newRow", "target": "Competitions", "values": {"Name": "C"}}
        ]
    ),
    (
        competitions_newrow,
        "Competitions",
        {"Name": "D"},
        1,
        [
            {"event": "newRow", "target": "Competitions", "values": {"Name": "D"}}
        ]
    ),
    (
        competitors_newrow,
        "Competitors",
        {"FirstNames": "FNA", "LastName": "LNA", "CompetitionID": 2},
        1,
        [
            {"event": "newRow", "target": "Competitors", "values": {"FirstNames": "FNA", "LastName": "LNA"}}
        ]
    ),
    (
        competitors_newrow,
        "Competitors",
        {"FirstNames": "FNA", "LastName": "LNA", "CompetitionID": 1},
        2,
        [
            {"event": "newRow", "target": "Competitors", "values": {"FirstNames": "FNA", "LastName": "LNA"}},
            {"event": "newRow", "target": "CurrentCompetitors", "values": {"FirstNames": "FNA", "LastName": "LNA"}}
        ]
    )
])
def test_newrow(setup_and_teardown, function: callable, target: str, values: dict, expected_resp_count: int, expected_response_filters: list):
    responses = function({"event": "newRow", "target": target, "values": values}, client)
    assert len(responses) == expected_resp_count
    for e in expected_response_filters:
        print(f"{e}, {responses}")
        assert any(match_dicts(r, e) for r in responses)

@pytest.mark.parametrize("function, target, elem_id, expected_resp_count, expected_response_filters", [
    (
        competitions_rmrow,
        "Competitions",
        1,
        2,
        [
            {
                "event": "rmRow",
                "target": "Competitions"
            },
            {
                "event": "tableOverwritten",
                "target": "CurrentCompetitors"
            }
        ]
    ),
    (
        competitors_rmrow,
        "Competitors",
        2,
        1,
        [
            {
                "event": "rmRow",
                "target": "Competitors",
                "id": 2
            }
        ]

    ),
    (
        competitors_rmrow,
        "Competitors",
        1,
        2,
        [
            {
                "event": "rmRow",
                "target": "Competitors",
                "id": 1
            },
            {
                "event": "rmRow",
                "target": "CurrentCompetitors",
                "id": 1
            }
        ]
    )
])
def test_rmrow(setup_and_teardown, function: callable, target: str, elem_id: int, expected_resp_count: int, expected_response_filters: list):
    resp = function({"event": "rmRow", "target": target, "id": elem_id}, client)
    assert len(resp) == expected_resp_count
    for e in expected_response_filters:
        print(f"{e}, {resp}")
        assert any(match_dicts(r, e) for r in resp)


@pytest.mark.parametrize("function, target, elem_id, values, expected_resp_count, expected_response_filters", [
    (
        competitions_rowmodified,
        "Competitions",
        1,
        {
            "IsActive": False
        },
        2,
        [
            {
                "event": "rowModified",
                "target": "Competitions",
                "id": 1,
                "values": {

                }
            }
        ]
    ),
    (
        competitors_rowmodified,
        "Competitors",
        1,
        {
            "LastName": "LastNameA_1.0"
        },
        2,
        [
            {
                "event": "rowModified",
                "target": "Competitors",
                "id": 1,
                "values": {
                    "LastName": "LastNameA_1.0"
                }
            },
            {
                "event": "rowModified",
                "target": "CurrentCompetitors",
                "id": 1,
                "values": {
                    "LastName": "LastNameA_1.0"
                }
            }
        ]
    )
])
def test_rowmodified(setup_and_teardown, function: callable, target: str, elem_id: int, values: dict, expected_resp_count: int, expected_response_filters: list):
    resp = function({"event": "rowModified", "target": target, "id": elem_id, "values": values}, client)
    assert len(resp) == expected_resp_count
