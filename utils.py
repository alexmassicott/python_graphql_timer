from flask import g


def getId():
    try:
        logged_in_user = g.user
    except AttributeError:
        return None
        
    id = logged_in_user.id
    if id:
        return id
