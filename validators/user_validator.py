import re


def validate(user):
    ok = True
    ok = ok and validate_email(user.email)

    return ok


def validate_email(user):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, user):
        return True

    return False
