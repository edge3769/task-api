import base64
from functools import wraps
from flask import request
from app.user_model import User

def cred(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            s = request.headers.get('auth')
            if s:
                s = s.encode('ascii')
                s = base64.b64decode(s)
                s = s.decode('ascii')
                s = s.split(':')
                username = s[0]
                password = s[1]
                print('dec', username, password)
                return f(*args, **kwargs, username=username, password=password)
            else:
                return {'error': 'no credentials provided'}
        except Exception as e:
            print('e', e)
            return {'error': 'something wrong with your credentials'}, 401
    return wrapper

def auth(return_user=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('auth')
            if not token:
                return {'error': 'No token provided'}, 401

            user = User.check_token(token)
            
            if not user:
                return {'error': 'Invalid token'}, 401
            if return_user:
                return f(*args, **kwargs, user=user)
            else:
                return f(*args, **kwargs)
        return wrapper
    return decorator
