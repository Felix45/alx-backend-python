import seed

def stream_users():
    ''' Returns users using a generator '''

    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row

    cursor.close()
    connection.close()