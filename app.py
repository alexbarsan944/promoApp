import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface
from flask_cors import CORS
from flask_pymongo import PyMongo

import routes.discounts_routes as discounts_routes
import routes.store_routes as store_routes
import routes.user_routes as user_routes
from middleware.auth_decorator import require_user_auth
from middleware.delete_routes_decorator import require_delete_key
from middleware.key_decorator import require_appkey
from middleware.store_decorator import require_store_auth
from routes.subscription_routes import get_subscription

load_dotenv()

# App config
app = Flask(__name__)
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config.from_object('config')
app.config.from_pyfile('config.py')

session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)
app.permanent_session_lifetime = timedelta(days=5)
# ------------------------------------------------------------------------
""" Mongo config """
# ------------------------------------------------------------------------
mongo = PyMongo(app)

# ------------------------------------------------------------------------
""" CORS config """
# ------------------------------------------------------------------------
CORS(app)
cors = CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": '*'
    }
})
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
""" Cookie route """


@app.after_request
def cookies(response):
    session.permanent = True
    same_cookie = session_cookie.dumps(dict(session))
    response.headers.add("Set-Cookie", f"session={same_cookie}; Secure; HttpOnly; Expires=None; SameSite=None; Path=/;")
    return response


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
""" User routes """


@app.route('/')
@require_user_auth
def hello_world():
    email = dict(session)['user_email']['email']
    return f'Hello, you are logged in as {email}!'


@app.route('/users/register', methods=['POST'])
def register():
    return user_routes.register_user(mongo)


@app.route('/users/login', methods=['POST', 'GET'])
def login():
    return user_routes.login_user(mongo)


@app.route('/users/logout', methods=['GET', 'POST'])
@require_user_auth
def logout():
    return user_routes.logout()


@app.route('/users/<user_id>/discounts', methods=['GET'])
@require_user_auth
def get_user_discounts(user_id):
    return user_routes.get_user_disc(mongo, user_id)


@app.route('/users/<store_name>', methods=['POST'])
@require_user_auth
def get_discounts_from_store(store_name):
    return user_routes.get_discounts_from_store(mongo, store_name)


@app.route('/users/<user_id>/stores/<store_id>', methods=['DELETE'])
@require_user_auth
def remove_user_discounts(user_id, store_id):
    return user_routes.remove_user_store_discounts(mongo, user_id, store_id)


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
""" Discount routes """


@app.route('/discounts/<discount_id>', methods=['GET'])
@require_appkey
def discount_get(discount_id):
    return discounts_routes.get_discount(mongo, discount_id)


@app.route("/discounts", methods=["POST"])
@require_appkey
def discount_create():
    """Route for creating a discount"""
    return discounts_routes.create(mongo)


@app.route("/discounts/<discount_id>", methods=["DELETE"])
@require_appkey
def discount_delete(discount_id):
    """Route for deleting a discount"""
    return discounts_routes.delete(discount_id, mongo)


@app.route("/discounts/<discount_id>", methods=["PUT"])
@require_appkey
def discount_update(discount_id):
    """Route for updating a discount"""
    return discounts_routes.update(discount_id, mongo)


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
""" Store routes """


@app.route('/stores', methods=['GET'])
@require_user_auth
def get_stores():
    """ [GET] Return all available stores """
    return store_routes.get_all_stores(mongo)


@app.route('/stores/<store_id>', methods=['GET'])
def get_store(store_id):
    """ [GET] Return a single store from ID """
    return store_routes.get_store(mongo, store_id)


@app.route('/stores/subscribe', methods=['POST'])
@require_store_auth
def get_key():
    return get_subscription(mongo)


@app.route('/stores/<store_id>/discounts', methods=['GET'])
def get_store_discounts(store_id):
    """ [GET] Return all the discounts that are associated with a store """
    return store_routes.get_store_discounts(mongo, store_id)


@app.route('/stores/register', methods=['POST'])
def register_store():
    """ [POST] Register route for stores """
    return store_routes.store_register(mongo)


@app.route('/stores/login', methods=['POST'])
def login_store():
    """ [POST] Login route for stores """
    return store_routes.login_store(mongo)


# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
""" Cloud function  """


@app.route("/api/discounts", methods=["DELETE"])
@require_delete_key
def discount_delete_auto():
    """ [DELETE] Route for deleting expired discounts """
    return discounts_routes.delete_auto(mongo)
