from flask import session, request, make_response


def store_login_required(func):
    """ Decorator for protected routes """

    response = {
        "redirected": 'To store login',
    }

    def wrapper(*args, **kwargs):
        if "store_id" not in session:
            return response  # TODO  use redirect() function here instead of returning response
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper
