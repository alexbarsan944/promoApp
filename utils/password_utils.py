from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def generate_hash(password_plain):
    return bcrypt.generate_password_hash(password_plain).decode('utf-8')


def verify_password(hashed_password, plain_password):
    return bcrypt.check_password_hash(hashed_password, plain_password)
