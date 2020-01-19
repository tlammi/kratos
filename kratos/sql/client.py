"""
SQL client
"""

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, NVARCHAR, Date, CHAR

from . import tableview
from . import util


class Client:
    """
    Wrapper for SQL interface
    """

    def __init__(self, url: str, debug=False):
        """
        Initialize

        :param url: URL used to reach the SQL database
        :param debug: Echo the operations if True
        """
        self._engine = create_engine(url, echo=debug)
        self._meta = MetaData()

        self._competitions = Table("Competitions", self._meta,
                                   Column("ID", Integer, primary_key=True),
                                   Column("Name", NVARCHAR),
                                   Column("CompetitionDate", Date))

        self._competitors = Table("Competitors", self._meta,
                                  Column("ID", Integer, primary_key=True),
                                  Column("CompetitionID", Integer),
                                  Column("CategoryID", Integer),
                                  Column("GroupID", Integer),
                                  Column("FirstNames", NVARCHAR),
                                  Column("LastName", NVARCHAR),
                                  Column("BodyWeight", Integer),
                                  Column("Sex", CHAR))

        self._attempts = Table("Attempts", self._meta,
                               Column("ID", Integer, primary_key=True),
                               Column("CompetitorID", Integer),
                               Column("Status", NVARCHAR),
                               Column("Number", Integer),
                               Column("Discipline", NVARCHAR),
                               Column("Result", Integer),
                               Column("Unit", NVARCHAR))

        self._meta.create_all(self._engine)
        self._conn = self._engine.connect()

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

    def attempts(self):
        """
        View of the attempts

        :return: TableView pointing to attempts
        """
        return tableview.TableView(self._attempts, self._conn, "ID")

    def get_active_competition_table(self, competition_id: int):
        """
        Helper method for acquiring table used for active competition management

        :param competition_id: Current competition ID, used for filtering the results
        :return: Tuple of (<list of column names>, <list of rows>)
        """
        query = sqlalchemy.text(
            f"""
            WITH
                snatches AS (SELECT * FROM Attempts WHERE Discipline = "Snatch"),
                snatch1 AS (SELECT * FROM snatches WHERE Number = 1),
                snatch2 AS (SELECT * FROM snatches WHERE Number = 2),
                snatch3 AS (SELECT * FROM snatches WHERE Number = 3),
                cjs AS (SELECT * FROM Attempts WHERE Discipline = "C&J"),
                cj1 AS (SELECT * FROM cjs WHERE Number = 1),
                cj2 AS (SELECT * FROM cjs WHERE Number = 2),
                cj3 AS (SELECT * FROM cjs WHERE Number = 3),
                flat_attempts AS (
                    SELECT 
                        snatch1.CompetitorID as "CompetitorID",
                        snatch1.Status AS "Snatch1Status",
                        snatch1.Result AS "Snatch1Result",
                        snatch1.Unit AS "Snatch1Unit",
                        snatch2.Status AS "Snatch2Status",
                        snatch2.Result AS "Snatch2Result",
                        snatch2.Unit AS "Snatch2Unit",
                        snatch3.Status AS "Snatch3Status",
                        snatch3.Result AS "Snatch3Result",
                        snatch3.Unit AS "Snatch3Unit",
                        cj1.Status AS "CJ1Status",
                        cj1.Result AS "CJ1Result",
                        cj1.Unit AS "CJ1Unit",
                        cj2.Status AS "CJ2Status",
                        cj2.Result AS "CJ2Result",
                        cj2.Unit AS "CJ2Unit",
                        cj3.Status AS "CJ3Status",
                        cj3.Result AS "CJ3Result",
                        cj3.Unit AS "CJ3Unit"
                    FROM snatch1 JOIN snatch2 ON snatch1.CompetitorID = snatch2.CompetitorID
                        JOIN snatch3 ON snatch2.CompetitorID = snatch3.CompetitorID
                        JOIN cj1 ON snatch3.CompetitorID = cj1.CompetitorID
                        JOIN cj2 ON cj1.CompetitorID = cj2.CompetitorID
                        JOIN cj3 ON cj2.CompetitorID = cj3.CompetitorID
                )
            SELECT *
            FROM Competitors JOIN flat_attempts ON Competitors.ID = flat_attempts.CompetitorID
            WHERE Competitors.CompetitionID = {competition_id}
            """
        )

        return util.sql_result_to_header_and_rows(self._conn.execute(query))
