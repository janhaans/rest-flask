from flask_restful import Resource, reqparse
from models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('passwd', type=str, required=True, help='Password is required')

    def post(self):
        data = User.parser.parse_args()
        
        try:
            user = UserModel.get_by_username(data['username'])
        except:
            return {'message': 'Could not create user, because of database error'}, 500
        
        if user:
            return {'message': f'User {user.username} is already registered'}, 400 
        
        try:
            UserModel.insert(data['username'],data['passwd'])
        except:
            return {'message': 'Could not create user, because of database error'}, 500
        
        return {'message': 'User created successfully'}, 201