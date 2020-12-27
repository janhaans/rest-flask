from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from user import User, UserRegister
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)
api = Api(app)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')

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
    def get(self):
        return {"items": items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

@app.route('/protected')
@jwt_required()
def protected():
    return f'{current_identity}', 200

app.run(host='0.0.0.0', port=5000)