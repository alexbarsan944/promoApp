import json

from flask import request, session

from middleware.generate_jwt import encode_auth_token
from models.keys import Key
from models.keys_enhanced import KeysEnhanced


def get_subscription(mongo):
    """ [GET] request for a protected route """

    def mapper(json):
        jwt = json["jwt"]
        return Key(jwt)

    def add_key(token):
        res = {
            "jwt": str(token),
        }
        user = mapper(res)
        inserted_id = mongo.db.keys.insert_one(user.to_json()).inserted_id
        saved_key = KeysEnhanced(user, inserted_id)
        return saved_key
        pass

    print(session)
    store_name = request.json.get('store_name')
    days = request.json.get('days')
    response = {}
    if store_name != session['store_name']:
        response["Response"] = "Store name and login credentials don't match"
        return json.dumps(response), 400
    if store_name and days:
        token = encode_auth_token(session['store_name'], days)
        add_key(token)
        response = {"JWT": token}
    else:
        response["response"] = "store_name or password not entered"
        return json.dumps(response), 400
    return json.dumps(response), 200
