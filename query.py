import graphene
from graphene import relay
from flask import g
from models import User as UserModel
from models import Session as SessionModel
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField


class ViewerQuery(graphene.ObjectType):
    node = relay.Node.Field()
    fields = graphene.Field(User, )
    sessions = PynamoConnectionField(Session)

    def resolve_fields(self, args, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None

        return logged_in_user

    def resolve_sessions(self, args, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None
        id = logged_in_user.id
        return [user for user in SessionModel.id_index.query(id)]


class UsersQuery(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User, id=graphene.List(graphene.String))

    def resolve_users(self, args, context, info):
        return [user for user in UserModel.batch_get(args['id'])]
