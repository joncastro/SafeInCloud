# DeSafe for Safe In Cloud

Desafe provides a python utility to decrypt a [SafeInCloud](www.safe-in-cloud.com) database file. It mainly provides a command line utility to be able to read labels and cards, and export the [SafeInCloud](www.safe-in-cloud.com) database in json or xml format.

For all options `desafe` command will prompt to enter the master password of the database file.

## Installation

* Using pip

```
pip install desafe
```

* From source

```
git clone https://github.com/joncastro/SafeInCloud
cd SafeInCloud
python setup.py install
```

### Printing cards

Desafe will print the cards that matches given filters. If filters are not provided all cards will be printed. By default, passwords will not be printed unless `-p` or `--password` option is given. Deleted items will be ignored too unless `-d` option is given.

Example of printing all cards:

`desafe card SafeInCloud.db`

Example of printing just the cards that match either gmail or facebook:

`desafe card gmail facebook SafeInCloud.db`

### Export database

The given file can be exported in `json` or `xml`. If `output-file` is not given, output will be printed to the standard output.

Example,

`desafe export SafeInCloud.db json SafeInCloud.json`

### Printing label

Global labels will be printed by given `label` and the database file. For example,

`desafe label SafeInCloud.db`

### Desafe help

For a complete description of the command utility, please refer to the usage.

```
$ desafe -h
Desafe for Safe In Cloud (safe-in-cloud.com).
A python utility to decrypt Safe In Cloud databases files

Usage:
  desafe card <file> [<filter>...] [-p] [-r] [-d]
  desafe label <file>
  desafe export <file> (json|xml) [<output-file>]
  desafe (-h | --help)

self.args:
  card    Print cards
  label   Print labels
  export  Exports given file in clear in the given format (json or xml).
  file    Safe in Cloud database file path
  filter  optional words to filter entries

Options:
  -p --password     Print passwords.
  -r --raw          Print information keeping the original format.
  -d --deleted      Included deleted items.
  -h --help         Show this screen.
  -v --version      Show version.
```
