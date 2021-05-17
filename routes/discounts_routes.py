from bson import ObjectId

from utils.json_encoder import encode


def get_discount(mongo, discount_id):
    discount = mongo.db.discounts.find_one({"_id": ObjectId(discount_id)})
    discount_json = {
        "storeId": discount['storeId'],
        "code": discount['code'],
        "_id": encode(discount['_id'])
    }
    discount_json["_id"] = discount_json["_id"][1:-1]
    return discount_json
