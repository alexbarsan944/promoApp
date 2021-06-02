import json

from bson import ObjectId
from flask import request, session

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
    store_name = request.json.get('store_name')

    store = mongo.db.stores.find_one({"email": email})
    name = mongo.db.stores.find_one({"store_name": store_name})
    if store or name:
        response['response'] = 'Email or store name already in use.'
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
    session.permanent = True
    inserted_id = mongo.db.stores.insert_one(store.to_json()).inserted_id
    saved_user = StoreEnhanced(store, inserted_id)

    session['store_id'] = str(inserted_id)
    session['store_name'] = saved_user.to_json()['store']

    return saved_user.to_json(), 201


def login_store(mongo):
    """ [POST] Login with store_name and password """

    response = {
        "success": False,
        "response": " "
    }
    email = request.json.get('email')
    password = request.json.get('password')
    if email and password:
        store = mongo.db.stores.find_one({"email": email})
        if store and verify_password(store['password'], password):
            session.permanent = True
            session['store_id'] = str(store['_id'])
            session['store_name'] = store['store_name']

            response["success"] = True
            response['id'] = str(store['_id'])
            response['response'] = str(store['key'])
            response['store_name'] = store['store_name']

            return json.dumps(response), 200
        else:
            response["response"] = "Wrong password"
            return json.dumps(response), 400
    else:
        response["response"] = "Email or password not entered."
        return json.dumps(response), 400
    pass


def get_store(mongo, store_id):
    """ [GET] Return a single store from ID """

    store_doc = mongo.db.stores.find_one({"_id": ObjectId(store_id)})
    response = {
        "success": False,
        "response": " "
    }
    if not store_doc:
        response['response'] = "No stores with the specified id."
        return response, 404

    store_json = {
        "store_name": store_doc['store_name'],
        "_id": encode(store_doc['_id'])
    }
    store_json["_id"] = store_json["_id"][1:-1]
    return store_json, 200


def get_all_stores(mongo):
    """ [GET] Return all available stores """

    store_doc = mongo.db.stores.find()
    response = {
        "success": False,
        "response": " "
    }
    if not store_doc:
        response['response'] = "No stores available."
        return response, 404

    store_json = {}
    for store in store_doc:
        store_json[encode(store['_id'])[1:-1]] = {
            "store_name": store['store_name'],
            'email': store['email']
        }
    return json.dumps(store_json), 200


def get_store_discounts(mongo, store_id):
    """ [GET] Return all the discounts that are associated with a store """

    discounts_doc = mongo.db.discounts.find()
    discount_json = {}
    response = {
        "success": False,
        "response": " "
    }
    if not discounts_doc:
        response['response'] = "No discounts at the moment."
        return response, 404

    for discount in discounts_doc:
        id = encode(discount['store_id'])[1:-1]
        if id == store_id:
            discount_json[encode(discount['_id'])[1:-1]] = \
                {
                    'store_id': store_id,
                    'data_expirare': discount['data_expirare'],
                    'procent': discount['procent'],
                    'gama_produs': discount['gama_produs']
                }

    return discount_json, 200
