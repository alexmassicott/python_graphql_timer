import graphene
from time import time
from math import floor
from graphene import relay
from flask import g
from models import User as UserModel
from models import SessionIdIndex as SessionModel
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField
from uuid import uuid4
from flask_jwt_extended import get_jwt_identity


class CreateSession(graphene.Mutation):
    class Input:
        time = graphene.Int(required=True)

    success = graphene.Boolean()
    goal = graphene.String()

    def mutate(self, args, context, info):
        goal = args.get('time')
        id = get_jwt_identity()
        ok = True
        try:
            lastsession = SessionModel.id_index.query(id,limit=1,scan_index_forward=False).next()
            if lastsession.result is "pending":
                lastsession.result = "failed"
                lastsession.save()
            session_item = SessionModel(sid=str(uuid4()), start_timestamp=floor(time()), result="pending", time=goal, uid=id)
            session_item.save()
            user = UserModel.get(id)
            user.sessions += 1
            user.save()
        except AttributeError:
            ok = False

        return CreateSession(goal=goal, success=ok)


class endSession(graphene.Mutation):
    class Input:
        result = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, args, context, info):
        result = args.get('result')
        id = get_jwt_identity()
        ok = True
        lastsession = SessionModel.id_index.query(id, limit=1, scan_index_forward=False).next()
        lastsession.end_timestamp = (floor(time()))
        lastsession.result = (result)
        lastsession.save()
        if result is "success":
            user = UserModel.get(id)
            user.completions += 1
            user.save()
        return endSession(success=ok)


class ViewerMutations(graphene.ObjectType):
    node = relay.Node.Field()
    createsession = CreateSession.Field()
    endsession = endSession.Field()


class UsersMutations(graphene.ObjectType):
    node = relay.Node.Field()
    timeline = graphene.List(User, id=graphene.List(graphene.String))
