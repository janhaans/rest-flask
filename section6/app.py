from flask import Flask
from flask_restful import Api
from resources.user import User
from resources.item import Item, Items
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)
api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(User, '/register')

@app.route('/protected')
@jwt_required()
def protected():
    return f'{current_identity}', 200

app.run(host='0.0.0.0', port=5000)