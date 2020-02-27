"""
Helper class for accessing SQL database
"""

import sqlalchemy
from sqlalchemy.sql.expression import func

from . import util


class TableView:
    """
    Class providing a view to a SQL table
    """

    def __init__(self, table, conn, index_column):
        """
        Init

        :param table: sqlalchemy table object
        :param conn: sqlalchemy connection object
        :param index_column: Column used for indexing in []-operator
        """
        self._table = table
        self._conn = conn
        self._index_col = index_column

    def to_list(self):
        """
        Get data as a list of dicts

        :return: List of dicts
        """
        s = sqlalchemy.select([self._table])
        res = self._conn.execute(s)
        return util.sql_result_to_dicts(res)

    def to_header_and_rows(self):
        """
        Get header row as list and list of tuples containing the data

        :return: Tuple of (<header row>, <data>)
        """
        s = sqlalchemy.select([self._table])
        res = self._conn.execute(s)
        return util.sql_result_to_header_and_rows(res)

    def __getitem__(self, item):
        """
        []-operator

        :param item: Item matching to an element in index column
        :return: The matching row
        """
        s = sqlalchemy.select([self._table]).where(getattr(self._table.c, self._index_col) == item)
        try:
            return util.sql_result_to_dicts(self._conn.execute(s))[0]
        except IndexError:
            raise IndexError(f"Could not find {item} on column {self._index_col}")

    def max_id(self):
        """
        Get the maximum ID in the table

        Max ID is given to the element that is added to the table latest.

        :return: Maximum ID
        """
        s = sqlalchemy.select([func.max(getattr(self._table.c, self._index_col))])
        res = self._conn.execute(s).fetchall()[0][0]
        if res is None:
            raise IndexError("Could not get max ID, table is likely empty")
        return res

    def append(self, **kwargs):
        """
        Append a row to the table

        :param kwargs: Columns and values appended
        :return: None
        """
        i = self._table.insert().values(**kwargs)
        self._conn.execute(i)

    def update(self, elem_id, **kwargs):
        """
        Update values in table
        """
        u = self._table.update().where(
            getattr(self._table.c, self._index_col) == elem_id).values(**kwargs)
        self._conn.execute(u)

    def where(self, expression: str):
        """
        Filter data pointed by the TableView and return list of dicts with the filtered data

        :param expression: SQl expression stored in a WHERE-part of the query
        :return: List of dicts with the filtered data
        """
        s = sqlalchemy.select([self._table]).where(sqlalchemy.text(expression))
        res = self._conn.execute(s)
        rows = res.fetchall()
        keys = res.keys()
        dicts = []
        for row in rows:
            dicts.append(dict(zip(keys, row)))
        return dicts

    def delete_all(self):
        """
        Delete all data from the table

        :return: None
        """
        d = self._table.delete()
        self._conn.execute(d)

    def delete(self, key):
        """
        Delete element in the given index

        :param key: Key pointing to index of the element to be deleted
        :return: None
        """
        d = self._table.delete().where(getattr(self._table.c, self._index_col) == key)
        self._conn.execute(d)
