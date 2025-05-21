#! ../venv/bin/python3.8
import sqlite3

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


@with_db_connection
def fetch_all_users(conn, query="SELECT * FROM users"):
    ''' Fetch all the user records in the database '''
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results

@with_db_connection
def get_user_by_id(conn, user_id):
    ''' Fetch user from the users database by userId'''
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    results = cursor.fetchone()

    return results

print(fetch_all_users())
user = get_user_by_id(9)
print(user)
