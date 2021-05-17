import datetime
import os

import jwt


def encode_auth_token(store_id, days):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days),
            'iat': datetime.datetime.utcnow(),
            'sub': store_id
        }
        return jwt.encode(
            payload,
            os.environ.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e
