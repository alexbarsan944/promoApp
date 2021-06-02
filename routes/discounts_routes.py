from bson import ObjectId
from flask import request
from flask import session

from mappers import discount_mapper
from models.discount_enhanced import DiscountEnhanced
from utils.json_encoder import encode
from utils.time_utils import expired
from validators import discount_validator


def get_discount(mongo, discount_id):
    response = {
        "success": False,
        "response": " "
    }

    discount = mongo.db.discounts.find_one({"_id": ObjectId(discount_id)})
    if discount is None:
        response['response'] = "No existing discount"
        return response, 404
    discount_json = {
        "store_id": discount['store_id'],
        "gama_produs": discount['gama_produs'],
        "procent": discount['procent'],
        "_id": encode(discount['_id'])
    }
    discount_json["_id"] = discount_json["_id"][1:-1]
    return discount_json


def create(mongo):
    discount = discount_mapper.from_json_to_object(request.json)

    if not discount_validator.validate(discount):
        return "Invalid discount data", 400

    discount.to_json()['store_id'] = session['store_id']
    inserted_id = mongo.db.discounts.insert_one(discount.to_json()).inserted_id
    saved_discount = DiscountEnhanced(discount, inserted_id)
    saved_discount.to_json()['store_id'] = session['store_id']

    return saved_discount.to_json(), 201


def update(discount_id, mongo):
    discount_to_update = discount_mapper.from_json_to_object(request.json)
    response = {
        "success": False,
        "response": " "
    }

    if not discount_validator.validate(discount_to_update):
        return "Invalid discount data", 400

    discount = mongo.db.discounts.find_one({"_id": ObjectId(discount_id)})
    if not discount:
        response['response'] = "No discount available with the given ID."
        return response, 404

    discount_to_update.to_json()['store_id'] = session['store_id']

    mongo.db.discounts.find_one_and_update({"_id": ObjectId(discount_id)},
                                           {"$set": discount_to_update.to_json()})

    updated_discount = DiscountEnhanced(discount_to_update, discount_id)

    return updated_discount.to_json(), 200


def delete(discount_id, mongo):
    mongo.db.discounts.delete_one({"_id": ObjectId(discount_id)})
    response = {
        "success": True,
        'response': f"discount with id = {discount_id} deleted successfully"
    }
    return response, 200


def delete_auto(mongo):
    response = {
        "success": False,
        "response": " "
    }
    discounts_docs = mongo.db.discounts.find()
    for discount in discounts_docs:
        if expired(discount['data_expirare']):
            delete(discount['_id'], mongo)

    response['success'] = True
    response['response'] = "Deleted all expired promotions"
    return response, 200
