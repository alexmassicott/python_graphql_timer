from flask import g
from graphene_pynamodb import PynamoObjectType
from models import User as UserModel
from models import Session as SessionModel
from graphene import relay


class User(PynamoObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

    @classmethod
    def get_node(self, id, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None
        return logged_in_user


class Session(PynamoObjectType):
    class Meta:
        model = SessionModel
        interfaces = (relay.Node,)
