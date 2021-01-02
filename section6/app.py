from flask import Flask
from flask_restful import Api
from resources.user import User
from resources.item import Item, Items
from resources.store import Store, Stores
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from db import db

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWT(app, authenticate, identity)
api = Api(app)

@app.before_first_request
def create_database():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Stores, '/stores')
api.add_resource(User, '/register')

@app.route('/protected')
@jwt_required()
def protected():
    return f'{current_identity}', 200

db.init_app(app)
app.run(host='0.0.0.0', port=5000)