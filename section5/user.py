import sqlite3
from flask_restful import Resource, reqparse

class User():
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

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('passwd', type=str, required=True, help='Password is required')

    def post(self):
        data = UserRegister.parser.parse_args()
        
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        
        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (data['username'], data['passwd']))
        
        connection.commit()
        connection.close()
        
        return {'message': 'User created successfully'}, 201