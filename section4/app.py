from flask import Flask, request
from flask_restful import Api, Resource #, reqparse
#from flask_jwt import JWT, jwt_required

app = Flask(__name__)
api = Api(app)

items=[]

class Item(Resource):
    def get(self, name):
        pass

    def post(self, name):
        if next(filter(lambda x: x['name']== name, items), None):
            return {'message': f'Item {name} is already in the list'}, 409
        data = request.get_json()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201

    def put(self, name):
        pass

    def delete(self, name):
        pass

class Items(Resource):
    pass

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

app.run(host='0.0.0.0', port=5000)