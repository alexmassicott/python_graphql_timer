import graphene
from graphene import relay
from operator import attrgetter
from flask import g
from models import User as UserModel
from models import Session as SessionModel
# from models import SessionIdIndex
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField
from utils import getId
from flask_jwt_extended import get_jwt_identity

class ViewerQuery(graphene.ObjectType):
    node = relay.Node.Field()
    fields = graphene.Field(User, )
    history = PynamoConnectionField(Session)

    def resolve_fields(self, args, context, info):
        id = get_jwt_identity()
        try:
            logged_in_user = UserModel.get(id)
        except AttributeError:
            return None
        return logged_in_user

    def resolve_history(self, args, context, info):
        id = get_jwt_identity()
        query = SessionModel.id_index.query(id,scan_index_forward=False)
        return [session for session in query]


class UsersQuery(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User, id=graphene.List(graphene.String))
    timeline = PynamoConnectionField(Session, feed=graphene.List(graphene.String))

    def resolve_users(self, args, context, info):
        query = UserModel.batch_get(args['id']);
        return [user for user in query]

    def resolve_timeline(self, args, context, info):
        feed = args['feed']
        u1 = [User(id=id) for id in feed]
        query = SessionModel.uid.is_in(*u1)
        newlist = sorted(SessionModel.scan(query), key=attrgetter('start_timestamp'), reverse=True)
        return newlist
