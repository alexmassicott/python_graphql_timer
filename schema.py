import graphene
from flask import g, jsonify
from flask_graphql import GraphQLView
from flask_jwt import jwt_required
from graphene import relay, resolve_only_args
from graphene_pynamodb import PynamoConnectionField, PynamoObjectType

from app import app
from models import User as UserModel



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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    viewer = graphene.Field(User, )
    users = graphene.Field(User, id=graphene.String() )

    def resolve_viewer(self, args, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None

        return logged_in_user

    def resolve_users(self, args, context, info):
        print args['id']
        return UserModel.get(args['id'])

schema = graphene.Schema(query=Query)


def graphql_token_view():
    view = GraphQLView.as_view('graphql', schema=schema, graphiql=bool(app.config.get("DEBUG", False)))
    view = jwt_required()(view)
    return view


app.add_url_rule('/me', view_func=graphql_token_view())


@app.route("/graphql-schema", methods=['GET'])
def graphql_schema():
    schema_dict = {'data': schema.introspect()}
    return jsonify(schema_dict)
