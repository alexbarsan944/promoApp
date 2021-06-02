import os
from functools import wraps

from flask import request, abort


def require_delete_key(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        token = request.args.get('key')
        if token is None:
            abort(401)
        if token == os.environ.get('DELETE_KEY'):
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
