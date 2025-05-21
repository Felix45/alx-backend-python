#! ../venv/bin/python3.8

import time
import sqlite3
from functools import wraps

db_path = 'users.db'

def with_db_connection(func):
    def wrapper(*args, **kwargs):
        ''' Connect to sqlite database and pass the connection to the function '''
        try:
            with sqlite3.connect(db_path) as conn:
                return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise e
    return wrapper

def retry_on_failure(retries=3, delay=1):
    ''' Retry decorator factory '''

    def decorator(func):
        @wraps(func)
        def wrapper(conn, *args, **kwargs):
            attempt = 0
            while attempt <= retries:
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    attempt += 1
                    if attempt > retries:
                        print("Max retries reached. Raising exception.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

users = fetch_users_with_retry()
print(users)