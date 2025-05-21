#! ../venv/bin/python3.8

import sqlite3 
from functools import wraps


query_cache = {}
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

def cache_query():
    def decorator(func):
        @wraps(func)
        def wrapper(conn, *args, **kwargs):
            try:
                key = kwargs["query"]
                print(key)
                if key in query_cache:
                    print("Cache hit...")
                    return query_cache[key]
                print("Cache miss...")
                query_cache[key] = func(conn, *args, **kwargs)
                return query_cache[key]
            except Exception as e:
                print(f"An error occured")
                raise
            
        return wrapper
    return decorator


@with_db_connection
@cache_query()
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")

users_again = fetch_users_with_cache(query="SELECT * FROM users")

users_again = fetch_users_with_cache(query="SELECT * FROM users")