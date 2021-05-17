import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def encode(o):
    return JSONEncoder().encode(o)


class KeysEnhanced:
    def __init__(self, jwt, _id):
        self.jwt = jwt
        self.id = _id

    def to_json(self):
        final_json = {"jwt": self.jwt,
                      "_id": encode(self.id)
                      }

        final_json["_id"] = final_json["_id"][1:-1]

        return final_json
