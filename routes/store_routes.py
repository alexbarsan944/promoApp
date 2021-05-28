import json

from bson import ObjectId
from flask import request, session, g

import validators.store_validator as store_validator
from mappers.store_mapper import from_json_to_object
from models.store_enhanced import StoreEnhanced
from utils.json_encoder import encode
from utils.password_utils import generate_hash, verify_password


def store_register(mongo):
    """ [POST] Registration of a store """
    response = {
        "success": False,
        "response": " "
    }
    email = request.json.get('email')

    store = mongo.db.stores.find_one({"email": email})
    if store:
        response['response'] = 'Email already in use.'
        return json.dumps(response), 400

    request.json["password"] = generate_hash(request.json["password"])
    request.json["key"] = None
    store = from_json_to_object(request.json)
    if not store_validator.validate(store):
        response = {
            "success": False,
            "response": "Invalid store data"
        }
        return response, 400

    inserted_id = mongo.db.stores.insert_one(store.to_json()).inserted_id
    saved_user = StoreEnhanced(store, inserted_id)

    return saved_user.to_json(), 201


def login_store(mongo):
    """ [POST] Login with store_name and password """

    response = {
        "success": False,
        "response": " "
    }
    store_name = request.json.get('store_name')
    password = request.json.get('password')
    if store_name and password:
        store = mongo.db.stores.find_one({"store_name": store_name})
        if store and verify_password(store['password'], password):
            session['store_id'] = str(store['_id'])
            session['store_name'] = store['store_name']

            response["success"] = True
            response['id'] = str(store['_id'])
            response['response'] = str(store['key'])

            return json.dumps(response), 200
        else:
            response["response"] = "Wrong password"
            return json.dumps(response), 400
    else:
        response["response"] = "store_name or password not entered"
        return json.dumps(response), 400
    pass


def before_req_func():
    """ before_request function """

    g.user = None
    if 'user_id' in session:
        g.user = session['user_id']


def get_store(mongo, store_id):
    store_doc = mongo.db.stores.find_one({"_id": ObjectId(store_id)})
    store_json = {
        "store_name": store_doc['store_name'],
        "_id": encode(store_doc['_id'])
    }
    store_json["_id"] = store_json["_id"][1:-1]
    return store_json


def get_all_stores(mongo):
    store_doc = mongo.db.stores.find()
    store_json = {}
    for store in store_doc:
        store_json[encode(store['_id'])[1:-1]] = {
            "store_name": store['store_name'],
            'email': store['email']
        }
    return json.dumps(store_json)
