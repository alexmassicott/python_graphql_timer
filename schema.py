import graphene
from flask import g, jsonify
from flask_graphql import GraphQLView
from flask_jwt import jwt_required
from graphene import relay, resolve_only_args
from graphene_pynamodb import PynamoConnectionField, PynamoObjectType

from app import app
from models import User as UserModel
from models import Session as SessionModel



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
        return [user for user in SessionModel.query(id)]

schema = graphene.Schema(query=ViewerQuery, types=[User, Session])

class UsersQuery(graphene.ObjectType):
    node = relay.Node.Field()
    users = graphene.List(User, id=graphene.List(graphene.String) )
    def resolve_users(self, args, context, info):
        result = UserModel.batch_get(args['id'])
        return [next(result) for i in args['id']]


schema2 = graphene.Schema(query=UsersQuery)


def me_view():
    view = GraphQLView.as_view('me', schema=schema, graphiql=bool(app.config.get("DEBUG", False)))
    view = jwt_required()(view)
    return view


def users_view():
    view = GraphQLView.as_view('users', schema=schema2, graphiql=bool(app.config.get("DEBUG", False)))
    view = jwt_required()(view)
    return view


app.add_url_rule('/me', view_func=me_view())
app.add_url_rule('/users', view_func=users_view())


@app.route("/", methods=['GET'])
def welcome():
    return "Hello World"


@app.route("/graphql-schema", methods=['GET'])
def graphql_schema():
    schema_dict = {'data': schema.introspect()}
    return jsonify(schema_dict)
