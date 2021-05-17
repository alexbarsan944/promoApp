import os

import jwt
from flask import session


def validate_jwt(token):
    decoded = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=["HS256"])
    exp = decoded['exp']
    iat = decoded['iat']
    sub = decoded['sub']

    if exp - iat <= 0:
        return "Expired key", 400
    if sub != session['user_id']:
        return "Key details and logged user don't match.", 400

    return "Success", 200
