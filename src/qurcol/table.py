"""
Internal. Functions to manipulate tables.

All functions in this module assume that input Tables are valid in a sense that
they contain same number of values in every column and consistent data types in
each column. This property is not validated in run time as it adds a
significant performance hit. Invalid tables may produce unpredictable behavior.
"""

from typing import Tuple

from . import Table


def truncate(
    table: Table, head_rows: int, tail_rows: int
) -> Tuple[Table, int]:
    """Truncates a `table` to only have at most `head_rows` in the beginning
    and `tail_rows` in the end of the resulting table, and a special row
    with `...` values in every cell to indicate that the table was truncated.
    Returns a truncated table and a number of truncated rows."""

    assert head_rows >= 0, "cannot keep a negative number of head rows"
    assert tail_rows >= 0, "cannot keep a negative number of tail rows"
    assert head_rows + tail_rows > 0, "truncated table would be empty"

    _, row_count = shape(table)

    # early exit if the table doesn't need to be truncated:
    if row_count <= head_rows + tail_rows:
        return table, 0

    result = {}
    for column_name in table:
        column = table[column_name]
        head = column[:head_rows]
        tail = column[-tail_rows:] if tail_rows > 0 else []
        result[column_name] = head + ["..."] + tail
    return result, row_count - head_rows - tail_rows


def shape(table: Table) -> Tuple[int, int]:
    column_names = list(table.keys())
    column_count = len(column_names)
    if column_count == 0:
        return 0, 0
    else:
        row_count = len(table[column_names[0]])
        return column_count, row_count
