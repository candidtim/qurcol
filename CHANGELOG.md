# qurcol changelog

## 1.0.0

### New features

 - Added `sql` command.


## 0.3.0

### New features

 - Added `--all` option to the `view` command.
 - Added `--output` option to the `schema` command.


## 0.2.0

### New features

 - Added CSV output format to the `view` command.

### Improvements

 - More robust command line interface.
 - Improved test coverage.


## 0.1.0 Initial version

### New features

 - POC of the "view file schema" feature.
 - POC of the "view file content" feature.


## Future improvements

These features are not yet implemented. This is a To-Do list with possible
features for the next releases.

### Selected

 - Configure CI.

 - Extensive testing with different input files. Test a case of complex
   (multi-column) indices in the input file.

### Candidates

 - Let users override how the date/time data types are mapped to SQLite.

 - Add SQL REPL.

 - Actually read only first/last chunks when --head/--tail arguments are
   defined for the "view" command.

 - Allow piping the input instead of only allowing a file path argument.
   Gracefully do nothing if no input (no file path, no pipe). Consider use
   case when combined with other tools (e.g. list files and pipe).

 - Pretty printing should consider the size of the output terminal. (?)

 - Make the style of output tables configurable. (?)

