import sqlite3

connection = sqlite3.connect('data/data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id int, username text, passwd text)'
cursor.execute(create_table)

users = [
    (1, 'user1', 'abcd'),
    (2, 'user2', 'efgh')
]
insert_users = 'INSERT INTO users VALUES (?, ?, ?)'
cursor.executemany(insert_users, users)

get_users = 'SELECT * FROM users'
for row in cursor.execute(get_users):
    print(row)

connection.commit()
connection.close()
