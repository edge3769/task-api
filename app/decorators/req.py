from functools import wraps
from flask import request

def req(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.json:
            req_json = request.json.get
        else:
            req_json = None
        req_args_get = request.args.get
        return f(*args, **kwargs, req_json=req_json)
    return wrapper