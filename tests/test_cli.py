import click
import click.testing
import pytest

from qurcol.cli import main, validate_non_negative_int


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_validate_positive_int():
    assert validate_non_negative_int(None, None, 0) == 0
    assert validate_non_negative_int(None, None, 1) == 1

    with pytest.raises(click.BadParameter):
        assert validate_non_negative_int(None, None, -1)


def assert_contains(container, is_in=[], not_in=[]):
    for e in is_in:
        assert e in container
    for e in not_in:
        assert e not in container


def test_view_default(runner, sample_file):
    result = runner.invoke(main, f"view --output=csv {sample_file}")
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["1,4", "2,5", "3,6"])


def test_view_all(runner, sample_file):
    result = runner.invoke(main, f"view --output=csv --all {sample_file}")
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["1,4", "2,5", "3,6"])


def test_view_head(runner, sample_file):
    result = runner.invoke(main, f"view --output=csv --head=1 {sample_file}")
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["1,4"], not_in=["2,5", "3,6"])


def test_view_tail(runner, sample_file):
    result = runner.invoke(main, f"view --output=csv --tail=1 {sample_file}")
    assert result.exit_code == 0
    assert_contains(result.output, not_in=["1,4", "2,5"], is_in=["3,6"])


def test_view_head_and_tail(runner, sample_file):
    result = runner.invoke(
        main, f"view --output=csv --head=1 --tail=1 {sample_file}"
    )
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["1,4", "3,6"], not_in=["2,5"])


def test_view_head_tail_validation(runner, sample_file):
    result = runner.invoke(main, f"view --head=0 --tail=0 {sample_file}")
    assert result.exit_code == 2
    assert "would be empty" in result.output


def test_view_head_tail_all_validation(runner, sample_file):
    result = runner.invoke(main, f"view --head=1 --all {sample_file}")
    assert result.exit_code == 2
    assert "mutually exclusive" in result.output


def test_view_truncate_note(runner, sample_file):
    result = runner.invoke(main, f"view --head=1 --tail=0 {sample_file}")
    assert result.exit_code == 0
    assert "2 rows are skipped" in result.output


def test_schema_without_metadata(runner, sample_file):
    result = runner.invoke(main, f"schema --output=csv {sample_file}")
    assert result.exit_code == 0
    assert_contains(
        result.output,
        is_in=["Name,Type,Nullable\n", "A,int64,True\n", "B,int64,True\n"],
        not_in=["Metadata"],
    )


def test_schema_with_metadata(runner, sample_file):
    result = runner.invoke(main, f"schema --output=csv --meta {sample_file}")
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["Name,Type,Nullable,Metadata\n"])


def test_sql_succeeds(runner, sample_file):
    result = runner.invoke(
        main, f"sql -c --output=csv {sample_file} 'SELECT * FROM data LIMIT 2'"
    )
    assert result.exit_code == 0
    assert_contains(result.output, is_in=["1,4", "2,5"], not_in=["3,6"])
