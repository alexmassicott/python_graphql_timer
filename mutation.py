import graphene
from graphene import relay
from flask import g
from models import User as UserModel
from models import Session as SessionModel
from meta import User, Session
from graphene_pynamodb import PynamoConnectionField


class CreateSession(graphene.Mutation):
    class Input:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    person = graphene.String()

    def mutate(self, args, context, info):
        person = args.get('name')
        ok = True
        return CreateSession(person=person, ok=ok)


class ViewerMutations(graphene.ObjectType):
    node = relay.Node.Field()
    sessions = CreateSession.Field()


class UsersMutations(graphene.ObjectType):
    node = relay.Node.Field()
    timeline = graphene.List(User, id=graphene.List(graphene.String))
