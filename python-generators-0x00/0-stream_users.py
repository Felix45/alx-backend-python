import mysql.connector

def stream_users():
    ''' Returns users using a generator '''

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row

    cursor.close()
    connection.close()