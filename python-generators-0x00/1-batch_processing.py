import seed

def stream_users_in_batches(batch_size=25):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    while True:
        records = cursor.fetchmany(batch_size)
        if not records:
            break
        yield records

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    ''' Processes records in batches of batch_size '''

    age = 25
    matched_users = []
    batches = stream_users_in_batches(batch_size)

    for batch in batches:
        for user in batch:
            if user['age'] > age:
                matched_users.append(user)
    
    return matched_users
