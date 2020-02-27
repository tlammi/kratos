"""
Helper class for accessing SQL tables
"""
import sqlalchemy
from sqlalchemy.sql.elements import TextClause


from . import util

class JoinedTableView:
    """
    Class used for accessing SQL tables that do not exsist in the database
    but are produced by joining other tables.
    """

    def __init__(self, query: TextClause, conn, index_col: str):
        """
        Init

        :param query: SQL query used to acquire the table
        :param conn: SQL connection that is already connected
        :param index_col: Column used for indexing operations in []-operator
        """
        self._query = query
        self._conn = conn
        self._index_col = index_col

    def to_list(self):
        """
        Returns contents of the table as a list of dicts

        :return: List of dicts with table data
        """
        return util.sql_result_to_dicts(self._conn.execute(self._query))

    def to_header_and_rows(self):
        """
        Get table data as a tuple of header and rows

        :return: tuple of list and list of lists,
            where the first values is a list representing the header
            and the second value a list of table rows
        """
        return util.sql_result_to_header_and_rows(self._conn.execute(self._query))

    def __getitem__(self, item):
        """
        []-operator
        """
        where_clause = f"{self._index_col} = {item}"
        return self.where(where_clause)[0]

    def where(self, where_clause: str):
        """
        Append a where clause to the query and return the result

        :param where_clause: WHERE clause
        :return: List of dicts containing the results
        """
        query = sqlalchemy.text(f"{self._query.text} WHERE {where_clause}")
        return util.sql_result_to_dicts(self._conn.execute(query))
