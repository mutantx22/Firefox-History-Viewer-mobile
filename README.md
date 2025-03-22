Firefox History Viewer 2025
===========================


Simple history extractor for Mozilla Firefox in Python. 

Requires:
- Linux
- Python 3+
- sqlite3
- jinja2
- Mozilla Firefox

Usage: 

`python firefoxHistoryViewer.py [-h] [-p PATH] -o OUT [-f {html,json}]`

Example:

	python firefoxHistoryViewer.py -p /path/to/places.sqlite -o history.json -f json
