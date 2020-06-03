import pytest

from qurcol.format import as_csv, as_text_table, format


tbl = {"A": [1, 2, 3], "B": [4, 5, 6]}


def test_as_csv():
    assert as_csv({}) == "\r\n"
    assert as_csv({"A": []}) == "A\r\n"
    assert as_csv({"A": [1]}) == "A\r\n1\r\n"
    assert as_csv({"A": [], "B": []}) == "A,B\r\n"
    assert as_csv(tbl) == "\r\n".join(["A,B", "1,4", "2,5", "3,6", ""])


def test_as_text_table():
    assert as_text_table({}) == ""
    # won't test various scenarios here because the code only calls the
    # underlying library with no data manipulation; only verifying that the
    # library was called:
    assert "--+--" in as_text_table(tbl)


def test_format():
    assert "A,B" in format(tbl, "csv")
    assert "--+--" in format(tbl, "table")

    with pytest.raises(AssertionError):
        format(tbl, "unknow")
