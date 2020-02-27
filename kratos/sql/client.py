"""
SQL client
"""

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, \
    Integer, NVARCHAR, Date, CHAR, Boolean

from . import joinedtableview
from . import tableview
from . import util


class Client:
    """
    Wrapper for SQL interface
    """


    CURRENT_COMPETITION_QUERY = sqlalchemy.text("""
    WITH
        CurrentCompetitions AS (SELECT * FROM Competitions WHERE IsActive = 1),
        CurrentCompetitors AS (
            SELECT
                Competitors.ID AS ID,
                Competitors.LastName AS LastName,
                Competitors.FirstNames AS FirstNames,
                Competitors.BodyWeight AS BodyWeight,
                Competitors.Sex AS Sex
            FROM
                Competitors JOIN CurrentCompetitions ON CurrentCompetitions.ID = Competitors.CompetitionID)
    SELECT
        *
    FROM
        CurrentCompetitors
    """)

    def __init__(self, url: str, debug=False):
        """
        Initialize

        :param url: URL used to reach the SQL database
        :param debug: Echo the operations if True
        """
        engine = create_engine(url, echo=debug)
        meta = MetaData()

        self._competitions = Table("Competitions", meta,
                                   Column("ID", Integer, primary_key=True),
                                   Column("Name", NVARCHAR),
                                   Column("CompetitionDate", Date),
                                   Column("IsActive", Boolean, default=False))

        self._competitors = Table("Competitors", meta,
                                  Column("ID", Integer, primary_key=True),
                                  Column("CompetitionID", Integer),
                                  Column("CategoryID", Integer),
                                  Column("GroupID", Integer),
                                  Column("LastName", NVARCHAR),
                                  Column("FirstNames", NVARCHAR),
                                  Column("BodyWeight", Integer),
                                  Column("Sex", CHAR))

        self._groups = Table("Groups", meta,
                             Column("ID", Integer, primary_key=True),
                             Column("CID", Integer),
                             Column("Name", NVARCHAR))

        self._categories = Table("Categories", meta,
                                 Column("ID", Integer),
                                 Column("Name", NVARCHAR))

        self._attempts = Table("Attempts", meta,
                               Column("ID", Integer, primary_key=True),
                               Column("CompetitorID", Integer),
                               Column("Status", NVARCHAR),
                               Column("Number", Integer),
                               Column("Discipline", NVARCHAR),
                               Column("Result", Integer),
                               Column("Unit", NVARCHAR))
        meta.create_all(engine)
        self._conn = engine.connect()

    def competitions(self):
        """
        View of the competitions

        :return: TableView pointing to competitions
        """
        return tableview.TableView(self._competitions, self._conn, "ID")

    def competitors(self):
        """
        View of the competitors

        :return: TableView pointing to competitors
        """
        return tableview.TableView(self._competitors, self._conn, "ID")

    def current_competitors(self):
        """
        View of current competitors

        The table handled via the View-object is produced as a join of
        competitors and competitions.
        """
        return joinedtableview.JoinedTableView(self.CURRENT_COMPETITION_QUERY, self._conn, "ID")

    def attempts(self):
        """
        View of the attempts

        :return: TableView pointing to attempts
        """
        return tableview.TableView(self._attempts, self._conn, "ID")
