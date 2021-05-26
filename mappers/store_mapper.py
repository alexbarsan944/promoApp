from models.store import Store


def from_json_to_object(json):
    username = json["store_name"]
    password = json["password"]
    email = json["email"]
    key = json['key']

    return Store(username, password, email, key)
