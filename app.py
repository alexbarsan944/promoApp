import os

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, session
from flask_pymongo import PyMongo

import routes.discounts_routes as discounts_routes
import routes.store_routes as store_routes
import routes.user_routes as user_routes
from middleware.auth_decorator import google_auth_required
from middleware.key_decorator import require_appkey
from middleware.store_decorator import store_login_required
from routes.subscription_routes import get_subscription

load_dotenv()

# App config
app = Flask(__name__)
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config.from_object('config')
app.config.from_pyfile('config.py')

# ------------------------------------------------------------------------
""" Mongo config """
# ------------------------------------------------------------------------
mongo = PyMongo(app)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.before_request
def before_request():
    return store_routes.before_req_func()


@app.route('/')
@google_auth_required
def hello_world():
    email = dict(session)['profile']['email']
    name = dict(session)['profile']['given_name']

    return f'Hello {name}, you are logged in as {email}!'


@app.route('/login', methods=['GET'])
def login():
    return user_routes.login_user(oauth)


@app.route('/logout', methods=['POST'])
def logout():
    return user_routes.logout()


@app.route('/authorize')
def authorize():
    return user_routes.authorize(oauth)


@app.route('/stores/register', methods=['POST'])
def register_store():
    return store_routes.store_register(mongo)


@app.route('/stores/login', methods=['POST'])
def login_store():
    return store_routes.login_store(mongo)


@app.route('/discounts/<discount_id>', methods=['GET'])
@require_appkey
def discount_get(discount_id):
    return discounts_routes.get_discount(mongo, discount_id)


@app.route('/stores/<store_id>', methods=['GET'])
@store_login_required
def get_store(store_id):
    return store_routes.get_store(mongo, store_id)


@app.route('/subscriptions', methods=['POST'])
@store_login_required
def get_key():
    return get_subscription(mongo)
