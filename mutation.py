import graphene
from time import time
from math import floor
from graphene import relay
from flask import g
from models import User as UserModel
from models import Session as SessionModel
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField
from uuid import uuid4
from utils import getId


class CreateSession(graphene.Mutation):
    class Input:
        goal = graphene.String(required=True)

    success = graphene.Boolean()
    goal = graphene.String()

    def mutate(self, args, context, info):
        goal = args.get('time')
        id = getId()
        ok = True
        try:
            session_item = SessionModel(sid=str(uuid4()), start_timestamp=floor(time()), result="pending", time=goal, id=id)
            session_item.save()
        except AttributeError:
            ok = False

        return CreateSession(goal=goal, success=ok)


class endSession(graphene.Mutation):
    class Input:
        result = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, args, context, info):
        result = args.get('result')
        id = getId()
        ok = True
        try:
            SessionModel.end_timestamp.set(floor(time()))
            SessionModel.result.set(result)
        except AttributeError:
            ok = False

        return endSession( success=ok)


class ViewerMutations(graphene.ObjectType):
    node = relay.Node.Field()
    createsession = CreateSession.Field()
    endsession = endSession.Field()


class UsersMutations(graphene.ObjectType):
    node = relay.Node.Field()
    timeline = graphene.List(User, id=graphene.List(graphene.String))
