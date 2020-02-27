
from unit.web.web import *
import sql
import json

def test_index():
    html = serve_index()
    assert "<html>" in html
    assert "</html>" in html

def test_favicon():
    favicon = serve_favicon()
    assert len(favicon.body.read()) > 0
    assert favicon.status == "200 OK"


def test_css():
    res = serve_css("default.css")
    assert res.status == "200 OK"
    res = serve_css("DOES_NOT_DEFINITELY_EXIST.css")
    assert res.status == "404 Not Found"

def test_js():
    res = serve_script("script.js")
    assert res.status == "200 OK"
    res = serve_script("asdfasfdasdfasdf")
    assert res.status == "404 Not Found"

def test_tables():
    client = sql.Client("sqlite:///:memory:")
    client.competitions().append(Name="A", IsActive=True)
    client.competitions().append(Name="B")
    client.competitors().append(FirstNames="FirstNamesA", LastName="LastNameA", CompetitionID=1)
    client.competitors().append(FirstNames="FirstNamesB", LastName="LastNamesB", CompetitionID=2)

    res = json.loads(serve_tables("Competitions", client))
    assert len(res["rows"]) == 2
    res = json.loads(serve_tables("Competitors", client))
    assert len(res["rows"]) == 2
    res = json.loads(serve_tables("CurrentCompetitors", client))
    assert len(res["rows"]) == 1
