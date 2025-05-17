#! ../venv/bin/python3.8

import seed

connection = seed.db_connection()

if connection:
    seed.create_database(connection)
    connection.close()
    
    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        connection.close()
    else:
        print("Could not connect to ALX_prodev database")
else:
    print("Could not establish connection to the server")
    