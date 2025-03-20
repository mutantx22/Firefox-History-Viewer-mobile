#!/usr/bin/env python3

import os
import sqlite3
import subprocess

def findPath():
    username = subprocess.run(["whoami"], capture_output=True, text=True).stdout.strip()
    path = f"/home/{username}/.mozilla/firefox/"
    path += [name for name in os.listdir(path) if name.endswith(".default")][0]
    path += "/places.sqlite"
    return path

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
        query = """
        SELECT title, url, datetime(last_visit_date/1000000, 'unixepoch', 'localtime') as time
        FROM moz_places 
        WHERE last_visit_date IS NOT NULL;
        """
        try:
            cursor = self._db.execute(query)
            for row in cursor:
                yield dict(row)
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e.args[0]}")

def main():
    print(findPath())
    rows = [row for row in DBReader()]
    for row in rows:
        print(row['title'])

if __name__ == "__main__":
    main()
