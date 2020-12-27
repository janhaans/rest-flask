from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name']== name, items), None)
        if item:
            return item, 200
        else:
            return {'message': f'Item {name} is not in the list'}, 404

    def post(self, name):
        if next(filter(lambda x: x['name']== name, items), None):
            return {'message': f'Item {name} is already in the list'}, 400
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name']== name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            item.append(item)
        return item, 201

    def delete(self, name):
        pass

class Items(Resource):

    @jwt_required()
    def get(self):
        return {"items": items}, 200