from functools import wraps

from flask import session


def user_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session)
        user_id = dict(session).get('user_id', None)
        user_email = dict(session).get('user_email', None)

        if user_id and user_email:
            return f(*args, **kwargs)
        return 'Please log in first.'

    return decorated_function
