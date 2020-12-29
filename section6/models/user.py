import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, name, password):
        self.id = _id
        self.username = name
        self.password = password
    
    def __str__(self):
        return f'User(id={self.id})'

    @classmethod
    def get_by_username(cls, username):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else: 
            user = None
        connection.close()
        return user

    @classmethod
    def get_by_id(cls, _id):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM users WHERE id = ?', (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else: 
            user = None
        connection.close()
        return user

    @classmethod
    def insert(cls, username, passwd):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        
        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (username, passwd))
        
        connection.commit()
        connection.close()