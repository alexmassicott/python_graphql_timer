import graphene
from flask import g, jsonify
from flask_graphql import GraphQLView
from flask_jwt import jwt_required
from graphene import relay
from app import app
from models import User as UserModel
from models import Session as SessionModel
from query import ViewerQuery, UsersQuery
from mutation import ViewerMutations
from meta import User, Session

schema = graphene.Schema(query=ViewerQuery, mutation=ViewerMutations, types=[User, Session])
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
