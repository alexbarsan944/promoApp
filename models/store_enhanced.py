import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def encode(o):
    return JSONEncoder().encode(o)


class StoreEnhanced:
    def __init__(self, store, _id):
        self.id = _id
        self.store = store

    def to_json(self):
        final_json = {"store": self.store.store_name,
                      "email": self.store.email,
                      "password": self.store.password,
                      "_id": encode(self.id)
                      }

        final_json["_id"] = final_json["_id"][1:-1]

        return final_json
