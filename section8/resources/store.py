from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        try:
            store = StoreModel.get_store(name)
        except:
            return {'message': 'Could not get store, because of database error'}, 500

        if store:
            return store.json(), 200
        return {'message': f'Store {name} is not in the database'}, 404
        
    def post(self, name):
        try:
            store = StoreModel.get_store(name)
        except:
            return {'message': 'Could not create store, because of database error'}, 500
        
        if store:
            return {'message': f'Store {name} is already in the database'}, 400
        
        new_store = StoreModel(name)

        try:
            new_store.save_store()
        except:
           return {'message': 'Could not save store, because of database error'}, 500

        return {'message': f'Store {name} is successfully saved'}, 201


    def delete(self, name):
        try:
            store = StoreModel.get_store(name)
        except:
            return {'message': 'Could not get store, because of database error'}, 500

        if store:
            try:
                store.delete_store()
            except:
                return {'message': 'Could not delete store, because of database error'}, 500

            return {'message': f'Store {name} is successfully deleted'}, 201
        else:
            return {'message': f'Store {name} is not in database'}, 404


class Stores(Resource):
    
    @jwt_required()
    def get(self):
        try:
            stores = StoreModel.get_stores()
        except:
            return {'message': 'Could not get stores, because of database error'}, 500

        return {"stores": [store.json() for store in stores]}, 200