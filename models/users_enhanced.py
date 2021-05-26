import json

from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def encode(o):
    return JSONEncoder().encode(o)


class UserEnhanced:
    def __init__(self, user, _id):
        self.id = _id
        self.user = user

    def to_json(self):
        final_json = {
            "name": self.user.name,
            "email": self.user.email,
            "password": self.user.password,
            "discounts": self.user.discounts,
            "_id": encode(self.id)
        }

        final_json["_id"] = final_json["_id"][1:-1]

        return final_json
