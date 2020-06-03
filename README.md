# qurcol - view, query and convert columnar storage files from command line

`qurcol` (as in "query columnar ...") is a tool that enables its users to
quickly explore the content of a file in a column-oriented storage format (like
[Apache Parquet](https://parquet.apache.org/), for example), using command line
only and without the need for more complex software like Spark or Pandas.

It allows viewing the file content, schema, querying the content with SQL and
converting the data to CSV.

This tool only targets the use case of a basic exploration of a file content.
The author believes that aforementioned Spark, Pandas, etc. should be used
instead in any scenario which goes beyond that.


## Features

Command line tool to:

 - view a columnar file content
 - print a columnar file schema
 - convert a columnar file to a CSV file
 - run SQL queries on the data from a columnar file

List of supported columnar file formats:

 - [Apache Parquet](https://parquet.apache.org/)

Users should be aware of the size of the source files and keep in mind that
the file is read in memory when being processed by this tool.


## Status

This software is generally available. This software is intended to be used in
command line by individual users. It is not intended for use in a production
environment.

The software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
software.



## Installation

Install from PyPI:

    pip install [--user] qurcol

Alternatively, you can download a release from the Release page in GitHub.


## Usage

Built-in help provides detailed usage information with examples:

    qurcol --help


Few examples are given below to demonstrate the usage. Please, refer to the
built-in help for all details though (it is not practical to keep a duplicate
of the "help" in this README).

Print an extract (few first rows, few last rows) of the file content:

    qurcol view [[--head=N] [--tail=N] | [--all]] [--output=table|csv] FILE

For example, view to the snippet of a file content:

    qurcol view FILE

or, export entire file in CSV format:

    qurcol --all --output=csv FILE > OUTPUT_FILE

Print the file schema:

    qurcol schema [--output=table|csv] FILE

Run an inline SQL query on the file content:

    qurcol sql -c FILE "QUERY"


### SQL syntax

`qurcol sql` command loads the file into an in-memory SQLite database. Therefore,
data types and SQL syntax are those of SQLite v.3. The command will attempt
its best to map the data types from the source file to the data types available
in SQLite, but users should be aware of the fact that SQLite data types are
often less expressive (for example, there is no data type to represent
date/time information).

Data is loaded into a table with the name `data`.

Finally, for a complete example, the following command:

    qurcol sql -c --output=csv FILE "select * from data"

will have same effect as:

    qurcol view --all --output=csv FILE


## Why?

Here are few sample use cases:

 - As a Data Engineer I want to review the schema of a file in a data
   lake, in order to consume them accordingly in my software.

 - As a Data Ops Engineer I want to review the content of the sample file from
   a data lake, in order to ensure that the data is being produced into it.

 - As a Data Engineer I want to query some data from a file in a data lake, in
   order to review/confirm the properties of the data I am going to use.

 - As a Product Manager I want to load into a spreadsheet the `.parquet` file
   shared with me by Data Science team, in order to review its content.


## Not features

For any tool it is equally important to know what can and and what cannot be
done with it. Following potential features were considered for inclusion but
decided to be not in the current scope of this tool, unless a clear use case is
defined for them.

 - Conversion to other "complex" data formats (e.g. Excel), because it will add
   more dependencies to the tool, while CSV can be imported to a spreadsheet
   easily.

 - Reading data from files in other "file systems" (HDFS, S3, etc.), because
   there exist command line tools to "dowload" data from these.

 - Any advanced data exploration and plotting, because there is no single way
   to do that. You may use a combination of [Jupyter](https://jupyter.org/),
   [Pandas](https://pandas.pydata.org/) and
   [Seaborn](https://seaborn.pydata.org/) instead, for example.

 - Any advanced form of querying the data that goes beyond SQL. You may use
   [Pandas](https://pandas.pydata.org/) or [Apache
   Spark](https://spark.apache.org/) instead, for example.


## Contributions

Contributions are very welcome. Please, feel free to submit an issue or create
a Pull Request.

### Development environment

This software is written in Python 3, and has a modern development environment
that depends on [Poetry](https://python-poetry.org/docs/) and
[Nox](https://nox.thea.codes/en/stable/).

Run all tests:

    nox -s tests

Or, to quickly run tests on a single Python version only:

    poetry run pytest --cov

Run linters:

    nox lint

Reformat code:

    nox -s black

Or, check code format without reformatting:

    nox -s black -- --check .

Full pre-commit check:

    nox

Note: Nox is configured to reuse virtualenvs by default; if you want to run Nox
in a clean environment, add `--no-reuse-existing-virtualenvs` argument.


### Criteria for Pull Requests

 - The PR should pass on CI. CI is configured to run all essential controls
   (tests, flake8, mypy, black). You can easily run same controls in a local
   development environment before the PR submission.

 - Beyond code formatting, please, try to stick to the overall code style, such
   as the choice of variable names, code structure, etc.


## License

Licensed under the [Apache License v2.0](http://www.apache.org/licenses/).
