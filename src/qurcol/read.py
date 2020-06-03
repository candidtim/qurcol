"""
Internal. Functions to read input files. In current version, only Parquet is
supported.
"""

import pyarrow.parquet as pq

from . import Schema, Table


def read_table(file_path: str) -> Table:
    return pq.read_table(file_path).to_pydict()


def read_schema(file_path: str) -> Schema:
    pa_schema = pq.read_table(file_path).schema
    names = []
    types = []
    nullables = []
    metadatas = []
    for field in pa_schema:
        names.append(field.name)
        types.append(field.type)
        nullables.append(field.nullable)
        metadatas.append(field.metadata)
    return (
        {
            "Name": names,
            "Type": types,
            "Nullable": nullables,
            "Metadata": metadatas,
        },
        pa_schema.metadata,
    )
