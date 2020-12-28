from resources.user import User
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = User.get_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    userid = payload['identity']
    return User.get_by_id(userid)