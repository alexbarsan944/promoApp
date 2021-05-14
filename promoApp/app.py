from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta

from middleware.auth_decorator import login_required
from dotenv import load_dotenv
import routes.user_routes as user_routes

load_dotenv()

# App config
app = Flask(__name__)
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

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


@app.route('/')
@login_required
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
