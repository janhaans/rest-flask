from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.get_item(name)
        except:
            return {'message': 'Could not get item, because of database error'}, 500

        if item:
            return item.json(), 200
        return {'message': f'Item {name} is not in the database'}, 400
        
    def post(self, name):
        try:
            item = ItemModel.get_item(name)
        except:
            return {'message': 'Could not create item, because of database error'}, 500
        
        if item:
            return {'message': f'Item {name} is already in the database'}, 400
        
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'])

        try:
            new_item.save_item()
        except:
           return {'message': 'Could not save item, because of database error'}, 500

        return {'message': f'Item {name} is successfully saved'}, 201

    def put(self, name):
        data = Item.parser.parse_args()

        try:
            item = ItemModel.get_item(name)
        except:
            return {'message': 'Could not save item, because of database error'}, 500

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])
           
        try:
            item.save_item()
        except:
            return {'message': 'Could not save item, because of database error'}, 500
        
        return {'message': f'Item {name} is successfully saved'}, 201 

    def delete(self, name):
        try:
            item = ItemModel.get_item(name)
        except:
            return {'message': 'Could not get item, because of database error'}, 500

        if item:
            try:
                item.delete_item()
            except:
                return {'message': 'Could not delete item, because of database error'}, 500

            return {'message': f'Item {name} is successfully deleted'}, 201
        else:
            return {'message': f'Item {name} is not in database'}, 400


class Items(Resource):
    
    @jwt_required()
    def get(self):
        try:
            items = ItemModel.get_items()
        except:
            return {'message': 'Could not get items, because of database error'}, 500

        return {"items": [item.json() for item in items]}, 200