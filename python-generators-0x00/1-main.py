from itertools import islice
stream_users = __import__('0-stream_users')

users = stream_users.stream_users()


for user in islice(users,6):
  print(user)
