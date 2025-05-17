import csv
import uuid
import mysql.connector

def db_connection():
    ''' Connect to the ALX_prodev mysql server '''

    conn = mysql.connector.connect(host="localhost", user="root", password="")
    print("connection successful")

    return conn

def connect_to_prodev():
    ''' Connect to the ALX_prodev database '''
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="ALX_prodev")

    return conn

def create_table(connection):
    ''' Create user_data table in database '''
    cursor = connection.cursor()
    SQL    = """ CREATE TABLE IF NOT EXISTS user_data(
                   user_id CHAR(36) NOT NULL PRIMARY KEY, 
                   name VARCHAR(255) NOT NULL, 
                   email VARCHAR(255) NOT NULL, 
                   age DECIMAL NOT NULL
                );
            """
    cursor.execute(SQL)
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, file):
    ''' Insert data to a database table using a CSV file '''
    cursor = connection.cursor()

    with open(file, newline='') as f:
        data = csv.DictReader(f)
        for row in data:
            cursor.execute("INSERT INTO user_data(user_id, name, email, age) VALUES(%s, %s, %s, %s)", 
                            (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
    cursor.close()


def create_database(connection):
    ''' Create the ALX_prodev database if does not exist '''

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    print("Database created successfuly")
    cursor.close()
