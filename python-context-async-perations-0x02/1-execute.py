#! ../venv/bin/python3.8

import sqlite3

db_path = '../python-decorators-0x01/users.db'

class ExecuteQuery:
    ''' 
       Establish database connection and execute 
       query through a context manager 
    '''

    def __init__(self, db_name, query, params=None):
        ''' Connect to database db_name '''
        self.query  = query
        self.params = params or ()
        self.conn   = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def __enter__(self):
        print("------------------------------------ Entering context ------------------------------------ ")
        return self.cursor.execute(self.query, self.params).fetchall()
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("------------------------------------ Exiting context ------------------------------------ ")
        if exc_type:
            print(f"Exception occurred: {exc_value}")
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()

params = (25,)
query = "SELECT * FROM users WHERE age > ?"
with ExecuteQuery(db_path, query, params) as results:
    for row in results:
        print(dict(row))