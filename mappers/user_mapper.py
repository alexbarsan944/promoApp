from models.users import User


def from_json_to_object(json):
    name = json["name"]
    email = json["email"]
    password = json["password"]
    discounts = json["discounts"]

    return User(name, email, password, discounts)
