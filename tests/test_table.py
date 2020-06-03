import pytest

from qurcol.table import shape, truncate


tbl = {"A": [1, 2, 3], "B": [4, 5, 6]}


def test_shape():
    assert shape({}) == (0, 0)
    assert shape({"A": []}) == (1, 0)
    assert shape(tbl) == (2, 3)


def test_truncate_empty_table():
    assert truncate({}, 1, 0) == ({}, 0)
    assert truncate({}, 0, 1) == ({}, 0)
    assert truncate({}, 1, 1) == ({}, 0)


def test_truncate_nominal():
    assert truncate(tbl, 3, 0) == (tbl, 0)
    assert truncate(tbl, 0, 3) == (tbl, 0)
    assert truncate(tbl, 3, 3) == (tbl, 0)
    assert truncate(tbl, 9, 9) == (tbl, 0)
    assert truncate(tbl, 1, 1) == ({"A": [1, "...", 3], "B": [4, "...", 6]}, 1)
    assert truncate(tbl, 2, 0) == ({"A": [1, 2, "..."], "B": [4, 5, "..."]}, 1)
    assert truncate(tbl, 0, 2) == ({"A": ["...", 2, 3], "B": ["...", 5, 6]}, 1)


def test_truncate_constraints():
    with pytest.raises(AssertionError):
        truncate({}, -1, 0)

    with pytest.raises(AssertionError):
        truncate({}, 0, -1)

    with pytest.raises(AssertionError):
        truncate({}, 0, 0)
