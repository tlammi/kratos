

def sql_result_to_dicts(result):
    """
    Converts sqlalchemy query result to list of dicts

    :param result: Result of SQL query
    :return: List of dicts with data from the result
    """
    rows = result.fetchall()
    keys = result.keys()
    dicts = []
    for row in rows:
        dicts.append(dict(zip(keys, row)))
    return dicts


def sql_result_to_header_and_rows(result):
    """
    Converts sqlalchemy query result to tuple of header and data

    :param result: Result of SQL query
    :return: Tuple of (<header>, <data>)
    """
    rows = result.fetchall()
    keys = result.keys()

    return list(keys), rows
