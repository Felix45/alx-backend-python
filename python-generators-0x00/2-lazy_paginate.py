import seed

def lazypaginate(page_size, offset=0):
    ''' 
        Fetchs paginated data from the users table
        using a generator to lazily load each page
    '''
    connection = seed.connect_to_prodev()
    cursor     = connection.cursor()
    try:
        while True:
            cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += page_size
    finally:
        cursor.close()
        connection.close()

def paginate_users(page_size, offset=0):
    ''' 
        Paginated data from the users table
        using a generator to lazily load each page
    '''
    pages = lazypaginate(page_size, offset)

    for page in pages:
        print(page, end="\n\n")
