import json

from bson import ObjectId
from flask import request, session

from mappers.store_mapper import from_json_to_object
from middleware.generate_jwt import encode_auth_token
from models.keys import Key
from models.keys_enhanced import KeysEnhanced
from models.store_enhanced import StoreEnhanced
from validators.store_validator import validate


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

    store_name = session['store_name']
    days = request.json.get('days')

    response = {}

    if store_name and days:
        token = encode_auth_token(session['store_id'], days)
        add_key(token)
        store = mongo.db.stores.find_one({"_id": ObjectId(session['store_id'])})

        store_to_update = from_json_to_object(store)

        if store_to_update.to_json()['key'] is not None:
            response = {
                "success": False,
                "response": "You already have a key"
            }
            return response, 400
        if not validate(store_to_update):
            response = {
                "success": False,
                "response": "Invalid store data"
            }
            return response, 400

        store_to_update.to_json()['key'] = token

        mongo.db.stores.find_one_and_update({"_id": ObjectId(session['store_id'])},
                                            {"$set": store_to_update.to_json()})

        updated_store = StoreEnhanced(store_to_update, session['store_id'])
        return updated_store.to_json()['key'], 200
    else:
        response["response"] = "Add a day count"
        return json.dumps(response), 400
