import seed

def lazypaginate(page_size, offset=0):
    ''' 
        Fetchs paginated data from the users table
        using a generator to lazily load each page
    '''
    connection = seed.connect_to_prodev()
    cursor     = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")

    while True:
        rows = cursor.fetchmany(page_size)
        if not rows:
            break
        yield rows
    cursor.close()
    connection.close()

def paginate_users(page_size, offset):
    ''' 
        Paginated data from the users table
        using a generator to lazily load each page
    '''
    pages = lazypaginate(page_size, offset)

    for page in pages:
        print(page, end="\n\n")
    return pages