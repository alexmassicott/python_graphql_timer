from flask import g

from models import User


def authenticate(id,password):
    try:
        user = User.get(id)
        if user:
            print user.id
    except StopIteration:
        return None

    if user:
        return user


def identity(payload):
    user_id = payload['identity']
    print user_id
    try:
        g.user = User.get(user_id, None)
        return g.user
    except User.DoesNotExist:
        return None
