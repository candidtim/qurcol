"""
Internal. Functions to use SQL on Tables.
"""

import sqlite3

import pyarrow as pa

from . import Schema, Table


TYPES_MAPPING = {
    pa.bool_(): "INTEGER",
    pa.int8(): "INTEGER",
    pa.int16(): "INTEGER",
    pa.int32(): "INTEGER",
    pa.int64(): "INTEGER",
    pa.uint8(): "INTEGER",
    pa.uint16(): "INTEGER",
    pa.uint32(): "INTEGER",
    pa.uint64(): "INTEGER",
    pa.float16(): "REAL",
    pa.float32(): "REAL",
    pa.float64(): "REAL",
    pa.binary(): "BLOB",
    pa.string(): "TEXT",
}


def create_table(schema: Schema, table: Table) -> sqlite3.Connection:
    """Create an SQLite database with a single table named "data", with a
    schema derived from a given file schema, and given file content loaded
    into it. Returns an SQLite connection instance."""
    connection = _create_table(schema)
    _load_table(connection, schema, table)
    return connection


def query(connection: sqlite3.Connection, query: str) -> Table:
    table: Table = {}
    cursor = connection.execute(query)
    for row in cursor:
        for column_name in row.keys():
            table.setdefault(column_name, []).append(row[column_name])
    return table


def _create_table(schema: Schema) -> sqlite3.Connection:
    schema_table, _ = schema  # this function doesn't use the metadata
    fields = [
        (name, _sql_type(pa_type))
        for name, pa_type in zip(schema_table["Name"], schema_table["Type"])
    ]
    fields_declaration = ", ".join(
        [f"{name} {sql_type}" for name, sql_type in fields]
    )
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(f"CREATE TABLE data ( {fields_declaration} )")
    return connection


def _load_table(connection: sqlite3.Connection, schema: Schema, table: Table):
    schema_table, _ = schema  # this function doesn't use the metadata
    field_names = ", ".join(schema_table["Name"])
    placeholders = ", ".join("?" * len(schema_table["Name"]))
    insert_query = (
        f"INSERT INTO data ( {field_names} ) VALUES ( {placeholders } )"
    )
    connection.executemany(insert_query, zip(*table.values()))


def _sql_type(pa_type) -> str:
    return TYPES_MAPPING.get(pa_type, "TEXT")
