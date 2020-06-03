import click

from .format import format
from .read import read_schema, read_table
from .sql import create_table, query as sql_query
from .table import truncate


def validate_non_negative_int(ctx, param, value):
    if value is not None and value < 0:
        raise click.BadParameter(
            f"value should be a zero or a positive integer, not {value}"
        )
    else:
        return value


@click.group(name="qurcol")
def main() -> None:
    pass


@main.command()
@click.argument(
    "file_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--head",
    "-h",
    type=int,
    callback=validate_non_negative_int,
    show_default=True,
    help="Number of rows to show in the head of the file",
)
@click.option(
    "--tail",
    "-t",
    type=int,
    callback=validate_non_negative_int,
    show_default=True,
    help="Number of rows to show in the tail of the file",
)
@click.option(
    "--all",
    "-a",
    "keep_all",
    is_flag=True,
    help="Do not truncate the output, keep all rows",
)
@click.option(
    "--output",
    "-o",
    "output_format",
    default="table",
    type=click.Choice(["table", "csv"], case_sensitive=False),
    help="Output format",
)
def view(file_path, head, tail, keep_all, output_format) -> None:

    # click doesn't provide means to know if the value was set by default or
    # was expliclty defined by the user; for this reason this code manages the
    # default values for head/tail/all options

    if keep_all and (head or tail):
        raise click.UsageError(
            "--head/--tail and --all are mutually exclusive"
        )

    should_truncate = not keep_all

    if should_truncate:
        if head is None and tail is None:
            # set defaults if the user didn't define any of the three options
            head = 10
            tail = 10
        elif head is None and tail is not None:
            head = 0
        elif tail is None and head is not None:
            tail = 0

    if should_truncate and head + tail == 0:
        raise click.UsageError(
            "truncated table would be empty with given head and tail values"
        )

    source_table = read_table(file_path)

    output_table, truncated_row_count = (
        truncate(source_table, head, tail)
        if should_truncate
        else (source_table, 0)
    )

    click.echo(format(output_table, output_format))
    if truncated_row_count > 0:
        click.echo(f"\n {truncated_row_count} rows are skipped")


@main.command()
@click.argument(
    "file_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--meta/--no-meta",
    "-m",
    "show_meta",
    default=False,
    help="Whether to show the schema metadata (metadata is shown as-is)",
)
@click.option(
    "--output",
    "-o",
    "output_format",
    default="table",
    type=click.Choice(["table", "csv"], case_sensitive=False),
    help="Output format",
)
def schema(file_path, show_meta, output_format) -> None:
    schema, metadata = read_schema(file_path)
    if not show_meta:
        del schema["Metadata"]
    click.echo(format(schema, output_format))
    if show_meta:
        click.echo(f"\nMetadata:\n{metadata}")


@main.command()
@click.argument(
    "file_path",
    nargs=1,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.argument("query", nargs=1, required=True, type=str)
@click.option(
    "-c",
    "inline",
    required=True,
    is_flag=True,
    help=(
        "If specified, read the SQL query from a non-optional query argument "
        "(this option is mandatory in current version)"
    ),
)
@click.option(
    "--output",
    "-o",
    "output_format",
    default="table",
    type=click.Choice(["table", "csv"], case_sensitive=False),
    help="Output format",
)
def sql(file_path, query, inline, output_format) -> None:
    schema = read_schema(file_path)
    table = read_table(file_path)
    connection = create_table(schema, table)
    query_result = sql_query(connection, query)
    click.echo(format(query_result, output_format))
