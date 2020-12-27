import sqlite3

connection = sqlite3.connect('data/data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE users (id INTEGER PRIMARY KEY, username text, passwd text)'
cursor.execute(create_table)

users = [
    ('user1', 'abcd'),
    ('user2', 'efgh')
]
insert_users = 'INSERT INTO users VALUES (NULL, ?, ?)'
cursor.executemany(insert_users, users)

get_users = 'SELECT * FROM users'
for row in cursor.execute(get_users):
    print(row)

connection.commit()
connection.close()
