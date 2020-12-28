import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')

    @classmethod
    def get_item(cls, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'id': row[0], 'name': row[1], 'price': row[2]}

    @classmethod
    def create_item(cls, item):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (NULL, ?, ?)'
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        try:
            item = Item.get_item(name)
        except:
            return {'message': 'Could not get item, there is an database error'}, 500

        if item:
            return item, 200
        return {'message': f'Item {name} is not in the database'}
        
    def post(self, name):
        try:
            item = Item.get_item(name)
        except:
            return {'message': 'Could create item, there is an database error'}, 500
        
        if item:
            return {'message': f'Item {name} is already in the database'}, 400
        
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}

        try:
            Item.create_item(new_item)
        except:
            return {'message': 'Could create item, there is an database error'}, 500

        return {'message': f'Item {name} is successfully created'}, 201

    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = {'name': name, 'price': data['price']}

        try:
            item = Item.get_item(name)
        except:
            return {'message': 'Could update item, there is an database error'}, 500

        if item:
            try:
                Item.update_item(updated_item)
            except:
                return {'message': 'Could update item, there is an database error'}, 500

            return {'message': f'Item {name} is successfully updated'}, 201
        else:
            try:
                Item.create_item(updated_item)
            except:
                return {'message': 'Could update item, there is an database error'}, 500

            return {'message': f'Item {name} is successfully created'}, 201
        

    def delete(self, name):
        try:
            Item.delete_item(name)
        except:
            return {'message': 'Could delete item, there is an database error'}, 500

        return {'message': f'Item {name} is successfully deleted'}, 201

class Items(Resource):
    
    @classmethod
    def get_items(cls):
        items = []
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        results = cursor.execute(query)
        for row in results:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return items

    @jwt_required()
    def get(self):
        try:
            items = Items.get_items()
        except Exception as e:
            return {f"message': 'Could not get items, there is an database error {e}"}, 500

        return {"items": items}, 200