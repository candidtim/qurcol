from qurcol.read import read_schema, read_table


def test_read_table(sample_file):
    table = read_table(sample_file)
    assert table == {"A": [1, 2, 3], "B": [4, 5, 6]}


def test_read_schema(sample_file):
    schema = read_schema(sample_file)
    assert schema == (
        {
            "Name": ["A", "B"],
            "Type": ["int64", "int64"],
            "Nullable": [True, True],
            "Metadata": [
                {b"PARQUET:field_id": b"1"},
                {b"PARQUET:field_id": b"2"},
            ],
        },
        None,
    )
