from user import User, username_mapping, userid_mapping
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid, None)