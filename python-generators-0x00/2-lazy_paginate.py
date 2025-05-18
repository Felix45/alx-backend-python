import seed

def lazy_paginate(page_size):
    ''' 
        Fetchs paginated data from the users table
        using a generator to lazily load each page
    '''
    connection = seed.connect_to_prodev()
    cursor     = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(page_size)
        if not rows:
            break
        yield rows
    cursor.close()
    connection.close()

def paginate_users(page_size, offset=0):
    ''' 
        Paginated data from the users table
        using a generator to lazily load each page
    '''
    pages = lazy_paginate(page_size)

    for page in pages:
        print(page, end="\n\n")
    return pages