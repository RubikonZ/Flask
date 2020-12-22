from flask import request, Blueprint, redirect, session, url_for
from requests_oauthlib import OAuth2Session
from flask.json import jsonify
from time import time
import json
import os

auth = Blueprint('auth', __name__)

# This information is obtained from DonationAlerts
dalerts_client_id = os.environ.get('DA_CLIENT_ID')
dalerts_client_secret = os.environ.get('DA_CLIENT_SECRET')
dalerts_authorization_base_url = 'https://www.donationalerts.com/oauth/authorize'
datoken_url = 'https://www.donationalerts.com/oauth/token'
dalerts_scope = ['oauth-donation-index']
redirect_uri_dalerts = 'http://localhost:5000/dalerts/callback'


# DONATION ALERTS
@auth.route('/dalerts/auth')
def dalerts_auth():
    dalerts = OAuth2Session(dalerts_client_id, scope=dalerts_scope)
    authorization_url, state = dalerts.authorization_url(dalerts_authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['dalerts_oauth_state'] = state
    return redirect(authorization_url)


@auth.route("/dalerts/callback", methods=['GET'])
def dalerts_callback():
    dalerts = OAuth2Session(dalerts_client_id, state=session['dalerts_oauth_state'])
    token = dalerts.fetch_token(datoken_url, client_secret=dalerts_client_secret, authorization_response=request.url)

    session['dalerts_oauth_token'] = token
    return jsonify({"token": token})
    # return redirect(url_for('auth.dalerts_json'))


@auth.route('/dalerts', methods=['GET'])
def dalerts_json():
    dalerts = OAuth2Session(dalerts_client_id, token=session['dalerts_oauth_token'])
    return jsonify(dalerts.get('https://www.donationalerts.com/api/v1/alerts/donations').json())


# TWITCH
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
twitch_authorization_base_url = 'https://id.twitch.tv/oauth2/authorize'
twitch_token_url = 'https://id.twitch.tv/oauth2/token'
twitch_scope = ['chat:read', 'whispers:edit', 'chat:edit']
redirect_uri = 'http://localhost:5000/twitch/callback'
refresh_url = twitch_token_url


@auth.route("/twitch/auth")
def twitch_auth():
    twitch = OAuth2Session(twitch_client_id, scope=twitch_scope, redirect_uri=redirect_uri)
    authorization_url, state = twitch.authorization_url(twitch_authorization_base_url)

    # State is used to prevent CSRF
    session['twitch_oauth_state'] = state
    return redirect(authorization_url)


@auth.route("/twitch/callback", methods=['GET'])
def twitch_callback():
    twitch = OAuth2Session(twitch_client_id, state=session['twitch_oauth_state'], redirect_uri=redirect_uri)
    token = twitch.fetch_token(token_url=twitch_token_url, client_secret=twitch_client_secret, include_client_id=True, authorization_response=request.url)

    session['oauth_token'] = token

    with open('storage.json', 'w') as json_file:
        json.dump(token, json_file)

    return jsonify(token)
    # return redirect(url_for('auth.twitch_json'))


@auth.route('/twitch/refresh', methods=['GET'])
def twitch_refresh():
    token = session['oauth_token']

    twitch = OAuth2Session(twitch_client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    new_token = twitch.refresh_token(twitch_token_url, refresh_token=token['refresh_token'], client_id=twitch_client_id,
                                     client_secret=twitch_client_secret)
    return new_token


@auth.route('/twitch', methods=['GET'])
def twitch_json():
    twitch = OAuth2Session(twitch_client_id, token=session['twitch_oauth_token'])
    return jsonify(twitch.get('https://id.twitch.tv').json())


# GITHUB
github_client_id = os.environ.get('GITHUB_CLIENT_ID')
github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
github_authorization_base_url = 'https://github.com/login/oauth/authorize'
github_token_url = 'https://github.com/login/oauth/access_token'


@auth.route('/github/auth')
def github_auth():
    github = OAuth2Session(github_client_id, redirect_uri='http://localhost:5000/github/callback')
    authorization_url, state = github.authorization_url(github_authorization_base_url)

    session['github_oauth_state'] = state
    return redirect(authorization_url)


@auth.route('/github/callback')
def github_callback():
    github = OAuth2Session(github_client_id, state=session['github_oauth_state'])
    token = github.fetch_token(github_token_url, client_secret=github_client_secret, authorization_response=request.url)

    session['github_token'] = token
    return redirect(url_for('auth.github_json'))


@auth.route('/github')
def github_json():
    github = OAuth2Session(github_client_id, token=session['github_token'])
    return jsonify(github.get('https://api.github.com/user').json())
