import re


def validate(store):
    ok = True
    ok = ok and validate_email(store.email)

    return ok


def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True

    return False
