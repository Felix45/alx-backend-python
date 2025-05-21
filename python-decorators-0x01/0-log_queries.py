#! ../venv/bin/python3.8

import sqlite3
import functools
from faker import Faker
from datetime import datetime

def log_queries(func):
    ''' Decorator to log SQL queries '''
    def wrapper(*args, **kwargs):
        print(f"[SQL LOG] Args: {args} Kwargs: {kwargs} logged at: {datetime.now()}")
        result = func(*args,  **kwargs)
        return result
    return wrapper

def connect_to_database():
    ''' Connect to users sqlite database '''
    return sqlite3.connect('users.db')


@log_queries
def create_table(query):
    ''' Create the users table '''

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()



@log_queries
def insert_records(query, values):
    ''' Insert records in the users table '''

    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()


    
@log_queries
def fetch_all_users(query):
    ''' Fetch all the user records in the database '''
    connection  = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

create_table("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
insert_records("INSERT INTO users (name) VALUES (?)", (Faker().name(),))
users = fetch_all_users(query="SELECT * FROM users")
print(users)