#!/usr/bin/env python3

from modules.reporter import HTMLreporter
from modules.database import DBReader
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Firefox History Viewer")
    parser.add_argument('-p', '--path', type=str, help='Path to places.sqlite file (default is the one from the current user)')
    parser.add_argument('-o', '--out', type=str, required=True, help='Generated report file')
    args = parser.parse_args()

    dbPath = args.path
    reportPath = args.out

    try:
        db = DBReader(dbPath)
        htmlReporter = HTMLreporter()
        htmlReporter.report([row for row in db], reportPath)
        db.close()
    except ValueError as e:
        print(f"Error: {e.args[0]}")
        parser.print_usage()
    except Exception as e:
        print(f"Unknown error: {e}")
        parser.print_usage()

if __name__ == "__main__":
    main()
