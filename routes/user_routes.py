from flask import url_for, session, redirect


def login_user(oauth):
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


def authorize(mongo, oauth):
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    print(google)
    print(token)
    resp = google.get('userinfo')
    print(resp)
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info

    name = user['name']
    email = user['email']
    sub = user['sub']
    user_object = {
        "sub": sub,
        "name": name,
        "email": email,
        "cards": []
    }
    session['profile'] = user_info
    session.permanent = True
    user_id = mongo.db.users.find_one({"sub": sub})
    if user_id is None:
        var = mongo.db.users.insert_one(user_object).inserted_id

    return redirect('/')
