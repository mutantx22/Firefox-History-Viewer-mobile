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
        # Step 1: Determine which column is available
        try:
            cursor = self._db.execute("PRAGMA table_info(moz_places);")
            columns = {row[1] for row in cursor.fetchall()}
        except sqlite3.DatabaseError as e:
            print(f"Database error during schema check: {e.args[0]}")
            return
        
        if 'last_visit_date_local' in columns:
            time_column = 'last_visit_date_local'
            time_source = 'utc'
            time_conversion = f"datetime({time_column}/1000, 'unixepoch', 'localtime')"
        elif 'last_visit_date' in columns:
            time_column = 'last_visit_date'
            time_source = 'utc'
            time_conversion = f"datetime({time_column}/1000000, 'unixepoch')"
        else:
            print("Neither 'last_visit_date_local' nor 'last_visit_date' column found.")
            return
        
        # Step 2: Construct and execute the query
        query = f"""
        SELECT 
            title, 
            url, 
            {time_conversion} as time,
            '{time_source}' as time_source
        FROM moz_places 
        WHERE {time_column} IS NOT NULL;
        """
        try:
            cursor = self._db.execute(query)
            for row in cursor:
                yield dict(row)
        except sqlite3.DatabaseError as e:
            print(f"Database error during query: {e.args[0]}")




def main():
    print(findPath())
    rows = [row for row in DBReader()]
    for row in rows:
        print(row['title'])

if __name__ == "__main__":
    main()
