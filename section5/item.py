import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'id': row[0], 'name': row[1], 'price': row[2]}, 200
        else:
            return {'message': f'Item {name} is not in the database'}, 404

    def post(self, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        
        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            connection.close()
            return {'message': f'Item {name} is already in the database'}, 400
        
        data = Item.parser.parse_args()
        
        query = 'INSERT INTO items VALUES (NULL, ?, ?)'
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        
        return {'message': f'Item {name} is successfully created'}, 201

    def put(self, name):
        data = Item.parser.parse_args()

        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            query = 'UPDATE items SET price=? WHERE name=?'
            cursor.execute(query, (data['price'], name))
        else:
            query = 'INSERT INTO items VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, data['price']))
        
        connection.commit()
        connection.close()
        
        return {'message': f'Item {name} is successfully created'}, 201
        

    def delete(self, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        
        return {'message': f'Item {name} is successfully deleted'}, 201

class Items(Resource):

    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        
        query = 'SELECT * FROM items'
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})

        connection.close()
        return {"items": items}, 200