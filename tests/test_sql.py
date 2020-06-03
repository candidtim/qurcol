import sqlite3

import pyarrow as pa
import pytest

from qurcol.sql import (
    _create_table,
    _load_table,
    _sql_type,
    create_table,
    query,
)


sample_schema = (
    {
        "Name": ["A", "B"],
        "Type": [pa.string(), pa.int64()],
        "Nullable": [True, True],
    },
    None,
)


@pytest.mark.parametrize(
    "test_query,expected_result",
    [
        ("SELECT * FROM data", {"A": ["a", "b"], "B": [1, 2]}),
        ("SELECT * FROM data WHERE 0 = 1", {}),
    ],
)
def test_query(test_query, expected_result):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("CREATE TABLE data (A TEXT, B INTEGER)")
    connection.execute("INSERT INTO data VALUES ('a', 1)")
    connection.execute("INSERT INTO data VALUES ('b', 2)")
    query_result = query(connection, test_query)
    assert query_result == expected_result


def test_create_empty_table():
    connection = _create_table(sample_schema)
    sql_schema = [
        tuple(row)
        for row in connection.execute("PRAGMA table_info(data)").fetchall()
    ]
    assert sql_schema == [
        (0, "A", "TEXT", 0, None, 0),
        (1, "B", "INTEGER", 0, None, 0),
    ]


@pytest.mark.parametrize(
    "source_data,expected_result",
    [({}, []), ({"A": ["a", "b"], "B": [1, 2]}, [("a", 1), ("b", 2)])],
)
def test_load_table(source_data, expected_result):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("CREATE TABLE data (A TEXT, B INTEGER)")
    _load_table(connection, sample_schema, source_data)
    loaded_data = [
        tuple(row)
        for row in connection.execute("SELECT * FROM data").fetchall()
    ]
    assert loaded_data == expected_result


def test_create_table():
    connection = create_table(sample_schema, {"A": ["a", "b"], "B": [1, 2]})
    loaded_data = [
        tuple(row)
        for row in connection.execute("SELECT * FROM data").fetchall()
    ]
    assert loaded_data == [("a", 1), ("b", 2)]


def test_sql_type():
    # won't test all types here because it will replicate the original source
    # code only; testing that different data types are generally taken into
    # account, and that unknown source data types defaul to TEXT
    assert _sql_type(pa.int64()) == "INTEGER"
    assert _sql_type(pa.float64()) == "REAL"
    assert _sql_type(pa.binary()) == "BLOB"
    assert _sql_type(pa.string()) == "TEXT"
    assert _sql_type(pa.date64()) == "TEXT"
