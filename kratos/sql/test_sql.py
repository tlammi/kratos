import datetime
import pytest

from sql import Client

client = Client("sqlite:///:memory:")

@pytest.fixture()
def setup_and_teardown():
    client.competitions().append(**{
        "Name": "A",
        "CompetitionDate": datetime.date(2020, 2, 2)
    })
    client.competitions().append(**{
        "Name": "B",
        "CompetitionDate": datetime.date(2020, 3, 4)
    })

    client.competitors().append(**{
        "CompetitionID": 1,
        "LastName": "LastNameA",
        "FirstNames": "FirstNamesA",
        "BodyWeight": 80000,
        "Sex": "M"
    })
    client.competitors().append(**{
        "CompetitionID": 1,
        "LastName": "LastNameB",
        "FirstNames": "FirstNamesB",
        "BodyWeight": 69690,
        "Sex": "M"
    })
    client.competitors().append(**{
        "CompetitionID": 2,
        "LastName": "LastNameC",
        "FirstNames": "FirstNamesC",
        "BodyWeight": 50890,
        "Sex": "F"
    })
    yield
    client.competitions().delete_all()
    client.competitors().delete_all()

def test_competitions(setup_and_teardown):
    val = client.competitions()[1]
    assert val["Name"] == "A"
    val = client.competitions()[2]
    assert val["Name"] == "B"

def test_competitors(setup_and_teardown):
    val = client.competitors()[1]
    assert val["LastName"] == "LastNameA"
    val = client.competitors()[2]
    assert val["LastName"] == "LastNameB"
    val = client.competitors()[3]
    assert val["LastName"] == "LastNameC"

def test_current_competitors(setup_and_teardown):
    val = client.current_competitors().to_list()
    assert len(val) == 0
    client.competitions().update(1, IsActive=True)
    val = client.current_competitors().to_list()
    assert client.current_competitors()[1]["LastName"] == \
        client.competitors()[1]["LastName"]
    assert len(val) == 2
    client.competitions().update(1, IsActive=False)
    client.competitions().update(2, IsActive=True)
    val = client.current_competitors().to_list()
    assert len(val) == 1

def test_where(setup_and_teardown):
    val = client.competitions().where("ID=1")
    assert len(val) == 1
    assert val[0]["Name"] == "A"
    val = client.current_competitors().where("ID=1")
    assert len(val) == 0
    client.competitions().update(1, IsActive=True)
    val = client.current_competitors().where("ID=1")
    assert val[0]["FirstNames"] == "FirstNamesA"

def test_to_list(setup_and_teardown):
    val = client.competitions().to_list()
    assert len(val) == 2
    val = client.competitors().to_list()
    assert len(val) == 3
    client.competitions().update(1, IsActive=True)
    val = client.current_competitors().to_list()
    assert len(val) == 2


@pytest.mark.parametrize("table, len_rows", [
    (client.competitions(), 2),
    (client.competitors(), 3),
    (client.current_competitors(), 2)
])
def test_to_header_and_rows(setup_and_teardown, table, len_rows, check_index=0, check_val="ID"):
    client.competitions().update(1, IsActive=True)
    header, rows = table.to_header_and_rows()
    assert header[check_index] == check_val
    assert len(rows) == len_rows
    assert len(rows[0]) == len(header)


@pytest.mark.parametrize("table, index", [
    (client.competitions(), 101),
    (client.competitors(), 102),
    (client.current_competitors(), 99)
])
def test_invalid_index(setup_and_teardown, table, index):
    with pytest.raises(IndexError):
        table[100]

@pytest.mark.parametrize("table, id_column", [
    (client.competitions(), "ID")
])
def test_max_id(setup_and_teardown, table, id_column):
    dicts = table.to_list()
    max_id = max([d[id_column] for d in dicts])
    assert max_id == table.max_id()
    table.delete(max_id)
    dicts = table.to_list()
    max_id = max([d[id_column] for d in dicts])
    assert max_id == table.max_id()

    table.delete_all()

    with pytest.raises(IndexError):
        table.max_id()
