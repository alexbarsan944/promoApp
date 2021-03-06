import json

from bson import ObjectId
from flask import session, redirect, request

import mappers.user_mapper as user_mapper
import validators.user_validator as user_validator
from models.users_enhanced import UserEnhanced
from utils.json_encoder import encode
from utils.password_utils import generate_hash, verify_password


def login_user(mongo):
    session.pop('user_id', None)
    response = {
        "success": False,
        "response": " "
    }
    email = request.json.get('email')
    password = request.json.get('password')

    if email and password:
        user = mongo.db.users.find_one({"email": email})
        if not user['discounts']:
            user['discounts'] = []
        if user and verify_password(user['password'], password):
            session.permanent = True
            session['user_id'] = str(user['_id'])
            session['user_email'] = user['email']

            response["success"] = True
            response["response"] = str(user["_id"])
            response["name"] = user['name']

            store_name_set = set()

            for idx, discount in enumerate(user['discounts']):
                store_name_set.add(discount['store_name'])
            for store in store_name_set:
                store_doc = mongo.db.stores.find_one({"store_name": store})
                if store_doc:
                    user_id = str(user['_id'])
                    store_id = encode(store_doc['_id'])[1:-1]
                    subscribe(mongo, user_id, store_id)  # get new discounts

            user = mongo.db.users.find_one({"email": email})
            response["discounts"] = user['discounts']

            return json.dumps(response), 200
        else:
            response["response"] = "Wrong email or password"
            return json.dumps(response), 400
    else:
        response["response"] = "Email or password not entered"
        return json.dumps(response), 400
    pass


def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


def register_user(mongo):
    response = {
        "success": False,
        "response": " "
    }
    email = request.json.get('email')

    user = mongo.db.users.find_one({"email": email})
    if user:
        response['response'] = 'Email already in use.'
        return json.dumps(response), 400

    request.json["password"] = generate_hash(request.json["password"])
    request.json["discounts"] = []
    user = user_mapper.from_json_to_object(request.json)
    if not user_validator.validate(user):
        response = {
            "success": False,
            "response": "Invalid user data"
        }
        return response, 400

    inserted_id = mongo.db.users.insert_one(user.to_json()).inserted_id
    saved_user = UserEnhanced(user, inserted_id)

    return saved_user.to_json(), 201


def subscribe(mongo, user_id, store_id):
    """ [POST] Get all the discounts form <store_name> and append to user object"""

    def update(email, store_name, discounts_array):
        """ Update the user with the new discounts from store """

        user = mongo.db.users.find_one({"email": email})
        user_id = user['_id']
        user_to_update = user_mapper.from_json_to_object(user)

        if user_to_update.to_json()['discounts'] is not None:
            user_to_update.to_json()['discounts'] = list(
                filter(lambda x: not x['store_name'] == store_name, user_to_update.to_json()['discounts']))
            for item in discounts_array:
                user_to_update.to_json()['discounts'].append(item)
        else:
            user_to_update.to_json()['discounts'] = discounts_array

        print(discounts_array)
        mongo.db.users.find_one_and_update({"_id": user_id},
                                           {"$set": user_to_update.to_json()})

        updated_user = UserEnhanced(user_to_update, user_id)

        return updated_user.to_json(), 200

    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    store_doc = mongo.db.stores.find_one({"_id": ObjectId(store_id)})
    response = {
        "success": False,
        "response": " "
    }

    if not user_doc:
        response['response'] = 'No existing user with that ID.'
        return response, 404
    if not store_doc:
        response['response'] = 'No existing store with that ID.'
        return response, 404

    store_id = store_doc['_id']
    discounts = mongo.db.discounts.find({"store_id": str(store_id)})
    if discounts is None:
        response = {
            "success": False,
            "response": "No existing discount"
        }
        return response, 404
    discounts_to_send = []

    for discount in discounts:
        discounts_to_send.append({
            'discount_id': encode(discount['_id'])[1:-1],
            "store_name": store_doc['store_name'],
            "gama_produs": discount['gama_produs'],
            "procent": discount['procent'],
            'data_expirare': discount['data_expirare']
        })

    if 'user_email' not in session or 'user_id' not in session:
        response = {
            "success": False,
            "response": "Not logged in."
        }
        return response, 404

    email = dict(session)['user_email']

    update(email, store_doc['store_name'], discounts_to_send)
    return json.dumps(discounts_to_send), 200


def get_user_disc(mongo, user_id):
    """ [GET] Returns the discounts of a <user_id> """

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    response = {
        "success": False,
        "response": " "
    }
    if not user:
        response['response'] = "No user with the specified ID."
        return response, 404

    return json.dumps(user['discounts'])


def remove_user_store_discounts(mongo, user_id, store_id):
    """ [DELETE] Remove all the discounts from a user that are asociated with a store """

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    store = mongo.db.stores.find_one({"_id": ObjectId(store_id)})
    response = {
        "success": False,
        "response": " "
    }

    if not user:
        response['response'] = 'No existing user with that ID.'
        return response, 404
    if not store:
        response['response'] = 'No existing store with that ID.'
        return response, 404

    user_to_update = user_mapper.from_json_to_object(user)
    store_name = store['store_name']
    discounts_to_update = user_to_update.to_json()['discounts']

    if discounts_to_update is not None:
        discounts_to_update = list(
            filter(lambda x: not x['store_name'] == store_name, user_to_update.to_json()['discounts']))
    else:
        response['response'] = 'User is not subscribed to this store.'
        return response, 400

    user_to_update.to_json()['discounts'] = discounts_to_update

    mongo.db.users.find_one_and_update({"_id": ObjectId(user_id)},
                                       {"$set": user_to_update.to_json()})

    response['response'] = 'Deleted successfully.'
    response['success'] = True

    return response, 200
