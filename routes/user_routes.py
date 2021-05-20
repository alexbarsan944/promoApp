from flask import url_for, session, redirect


def login_user(oauth):
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


def authorize(oauth):
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    print(google)
    print(token)
    resp = google.get('userinfo')
    print(resp)
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    print(user)
    session['profile'] = user_info
    session.permanent = True
    return redirect('/')
