from flask import Flask
from flask_restful import Api
from resources.user import User
from resources.item import Item, Items
from resources.store import Store, Stores
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity
from db import db
import os

password = os.getenv('POSTGRES_PASSWORD')
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@db/postgres'
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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)