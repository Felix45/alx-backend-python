import seed

def stream_user_ages():
    '''
      Fetch the age of all users one by one
    '''

    connection = seed.connect_to_prodev()
    cursor     = connection.cursor(dictionary=True)

    cursor.execute("SELECT age FROM user_data")

    while True:
        record = cursor.fetchone()
        if record is None:
            break
        yield record

    cursor.close()
    connection.close()

def calculate_average_age():
    ''' Computes the average age of all users in table user_data '''

    users, total, count = stream_user_ages(), 0, 0

    for user in users:
        count += 1
        total += user['age']
    
    if count == 0:
        print("No users found")
        return
    
    average_age = total // count
    print(f"Average age of users: {average_age}")

    