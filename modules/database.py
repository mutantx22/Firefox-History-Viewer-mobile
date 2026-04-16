#!/usr/bin/env python3

import os
import sqlite3
import subprocess
from datetime import datetime, timezone, timedelta

def findPath():
    username = subprocess.run(["whoami"], capture_output=True, text=True).stdout.strip()
    path = f"/home/{username}/.mozilla/firefox/"
    path += [name for name in os.listdir(path) if name.endswith(".default")][0]
    path += "/places.sqlite"
    return path

def convert_time(timestamp, is_microseconds=True):
    # Firefox timestamps are in microseconds or milliseconds
    if is_microseconds:
        ts = timestamp / 1_000_000
    else:
        ts = timestamp / 1000
    dt = datetime.fromtimestamp(ts).astimezone()
    return dt.strftime('%Y-%m-%d') + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + dt.strftime('%H:%M:%S')

def get_date_string(timestamp, is_microseconds=True):
    if is_microseconds:
        ts = timestamp / 1_000_000
    else:
        ts = timestamp / 1000
    dt = datetime.fromtimestamp(ts).astimezone()
    return dt.strftime('%B %d %Y')

class DBReader:
    def __init__(self, dbPath=None):
        if dbPath is None:
            self.dbPath = findPath()
        else:
            self.dbPath = dbPath

    @property
    def dbPath(self):
        return self._dbPath

    @dbPath.setter
    def dbPath(self, path):
        self._dbPath = path
        if not os.path.isfile(path):
            raise ValueError("Invalid path")
        self._db = sqlite3.connect(self._dbPath)
        self._db.row_factory = sqlite3.Row

    @dbPath.deleter
    def dbPath(self):
        self.close()

    def close(self):
        self._db.close()
        del self._dbPath

    def __iter__(self):
        try:
            cursor = self._db.execute("PRAGMA table_info(moz_places);")
            columns = {row[1] for row in cursor.fetchall()}
        except sqlite3.DatabaseError as e:
            print(f"Database error during schema check: {e.args[0]}")
            return
        
        if 'last_visit_date_local' in columns:
            time_column = 'last_visit_date_local'
            is_microseconds = False  # milliseconds
        elif 'last_visit_date' in columns:
            time_column = 'last_visit_date'
            is_microseconds = True   # microseconds
        else:
            print("No valid time column found in database.")
            return
        
        query = f"""
            SELECT title, url, {time_column} as raw_time
            FROM moz_places
            ORDER BY raw_time DESC;
        """
        
        invalid_rows = []
        
        try:
            cursor = self._db.execute(query)
            previous_date = None
        
            for row in cursor:
                raw_time = row['raw_time']
        
                # Handle NULL or invalid timestamps
                if raw_time is None:
                    invalid_rows.append(row)
                    continue
        
                try:
                    date_str = get_date_string(raw_time, is_microseconds)
                    formatted_time = convert_time(raw_time, is_microseconds)
                except Exception:
                    invalid_rows.append(row)
                    continue
        
                if date_str != previous_date:
                    yield {
                        'title': '',
                        'url': '',
                        'time': '',
                        'date_separator': date_str
                    }
                    previous_date = date_str
        
                yield {
                    'title': row['title'] if row['title'] else row['url'],
                    'url': row['url'],
                    'time': formatted_time
                }
        
            # 🔻 Add invalid/unknown section at the end
            if invalid_rows:
                yield {
                    'title': '',
                    'url': '',
                    'time': '',
                    'date_separator': 'Unknown / Invalid Date'
                }
        
                for row in invalid_rows:
                    yield {
                        'title': row['title'] if row['title'] else row['url'],
                        'url': row['url'],
                        'time': 'N/A'
                    }
        
        except sqlite3.DatabaseError as e:
            print(f"Database error during query: {e.args[0]}")


