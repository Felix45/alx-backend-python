#! ../venv/bin/python3.8

import sqlite3

class DatabaseConnection:
    ''' Establish database connection through a context manager '''

    def __init__(self, db_name):
        ''' Connect to database db_name '''
        self.conn = sqlite3.connect(db_name)

    def __enter__(self):
        print("------------------ Entering context ------------------ ")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        print("------------------ Exiting context ------------------ ")
        if exc_type:
            print(f"Exception occurred: {exc_value}")
        self.conn.close()

db_path = '../python-decorators-0x01/users.db'

with DatabaseConnection(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)