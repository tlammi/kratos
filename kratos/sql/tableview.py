"""
Helper class for accessing SQL database
"""

import sqlalchemy

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
        return self._conn.execute(s).fetchall()[0]

    def append(self, **kwargs):
        """
        Append a row to the table

        :param kwargs: Columns and values appended
        :return: None
        """
        i = self._table.insert().values(**kwargs)
        self._conn.execute(i)

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
