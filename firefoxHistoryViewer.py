#!/usr/bin/env python3

from modules.reporter import HTMLreporter, JSONreporter
from modules.database import DBReader
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Firefox History Viewer")
    parser.add_argument('-p', '--path', type=str, help='Path to places.sqlite file (default is the current user)')
    parser.add_argument('-o', '--out', type=str, required=True, help='Generated report file')
    parser.add_argument('-f', '--format', type=str, choices=['html', 'json'], default='html',
                       help='Output format: html or json (default: html)')
    args = parser.parse_args()

    dbPath = args.path
    reportPath = args.out
    output_format = args.format

    try:
        db = DBReader(dbPath)
        rows = [row for row in db]  # Collect rows once
        
        if output_format == 'html':
            reporter = HTMLreporter()
        elif output_format == 'json':
            reporter = JSONreporter()
        
        reporter.report(rows, reportPath)
        db.close()
    except ValueError as e:
        print(f"Error: {e.args[0]}")
        parser.print_usage()
    except Exception as e:
        print(f"Unknown error: {e}")
        parser.print_usage()

if __name__ == "__main__":
    main()
