import graphene
from graphene import relay
from flask import g
from models import User as UserModel
from models import Session as SessionModel
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField
from utils import getId


class ViewerQuery(graphene.ObjectType):
    node = relay.Node.Field()
    fields = graphene.Field(User, )
    sessions = PynamoConnectionField(Session)

    def resolve_fields(self, args, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None
        id = logged_in_user.id
        logged_in_user.sessions = SessionModel.id_index.count(id)
        logged_in_user.completions = SessionModel.id_index.count(id, SessionModel.result == "success")
        return logged_in_user

    def resolve_sessions(self, args, context, info):
        id = getId()
        return [session for session in SessionModel.id_index.query(id)]


class UsersQuery(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User, id=graphene.List(graphene.String))
    timeline = PynamoConnectionField(Session)

    def resolve_users(self, args, context, info):
        return [user for user in UserModel.batch_get(args['id'])]

    def resolve_timeline(self, args, context, info):
        query = (SessionModel.id == "23") | (SessionModel.id == "10100290096651598")
        return [session for session in SessionModel.scan(query)]
