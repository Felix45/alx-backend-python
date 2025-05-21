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

def transactional(func):
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Transaction failed rolled back: {e}")
            raise
    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

update_user_email(user_id=2, new_email='Crawford_Cartwright@hotmail.com')