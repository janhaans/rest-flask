import sqlite3

connection = sqlite3.connect('data/data.db')

cursor = connection.cursor()

create_user_table = 'CREATE TABLE users (id INTEGER PRIMARY KEY, username text, passwd text)'
cursor.execute(create_user_table)

create_items_table = 'CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price real)'
cursor.execute(create_items_table)

connection.commit()
connection.close()