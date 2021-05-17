from flask import session


def store_login_required(func):
    """ Decorator for protected routes """

    response = {
        "redirected": 'To login',
    }

    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return response  # TODO  use redirect() function here instead of returning response
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper
