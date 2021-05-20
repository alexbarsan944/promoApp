from functools import wraps

from flask import request, abort

from validators.jwt_validator import validate_jwt


# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        token = request.args.get('key')
        if token is None:
            abort(401)
        var = validate_jwt(token)

        if token and var[1] == 200:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function
