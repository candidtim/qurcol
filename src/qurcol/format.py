"""
Internal. Functions to format the tables as text for output.
"""

import csv
import io

from tabulate import tabulate

from . import Table


def as_csv(table: Table) -> str:
    out = io.StringIO()
    writer = csv.writer(out, dialect="excel")
    writer.writerow(table.keys())
    for row in zip(*table.values()):
        writer.writerow(row)
    return out.getvalue()


def as_text_table(table: Table) -> str:
    headers = table.keys()
    return tabulate(table, headers, tablefmt="presto")  # type: ignore


_formats = {"csv": as_csv, "table": as_text_table}


def format(table: Table, format: str) -> str:
    assert format in _formats, f"unknown format {format}"
    return _formats[format](table)
