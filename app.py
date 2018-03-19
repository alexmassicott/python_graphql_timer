import os
from flask import Flask, jsonify, request, g
from datetime import timedelta
from flask_cors import CORS
from models import User
from time import time
from math import floor
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)

app = Flask(__name__)

# Enable blacklisting and specify what kind of tokens to check
# against the blacklist

app.config['JWT_SECRET_KEY'] = 'uQd8h731dnQLOlvbONMMvjbs8-Ljx-jc1NH0Dw_'  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

blacklist = set()
# For this example, we are just checking if the tokens jti
# (unique identifier) is in the blacklist set. This could
# be made more complex, for example storing all tokens
# into the blacklist with a revoked status when created,
# and returning the revoked status in this call. This
# would allow you to have a list of all created tokens,
# and to consider tokens that aren't in the blacklist
# (aka tokens you didn't create) as revoked. These are
# just two options, and this can be tailored to whatever
# your application needs.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


# Standard login endpoint
@app.route('/login', methods=['POST'])
def login():
    id = request.json.get('id', None)
    # password = request.json.get('password', None)
    try:
        user = User.get(id)
        user.last_login = floor(time())
        user.save()
    except StopIteration:
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        newuser = User(id = id, name = name, email=email, role = "user", last_login = floor(time()))
        newuser.save()
    ret = {
        'access_token': create_access_token(identity=id, expires_delta=timedelta(days=7)),
        'refresh_token': create_refresh_token(identity=id, expires_delta=timedelta(days=7))
    }
    return jsonify(ret), 200


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


# Endpoint for revoking the current users access token
@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@app.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user_id = identity
    try:
        g.user = User.get(user_id, None)
    except User.DoesNotExist:
        return None

CORS(app)
