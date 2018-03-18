from flask import g

from models import User


def authenticate(id,password="None"):
    print "yo"
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
    try:
        g.user = User.get(user_id, None)
        return g.user
    except User.DoesNotExist:
        return None
