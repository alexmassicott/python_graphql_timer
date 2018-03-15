import graphene
from flask import jsonify
from graphene import relay
from graphene_pynamodb import PynamoConnectionField, PynamoObjectType
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel
import json


class Department(PynamoObjectType):

    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)


class Employee(PynamoObjectType):

    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)


class Role(PynamoObjectType):

    class Meta:
        model = RoleModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_employees = PynamoConnectionField(Employee)
    all_roles = PynamoConnectionField(Role)
    role = graphene.Field(Role)

    def resolve_all_employees(self, args, context, info):
        return [EmployeeModel.get("1db39853-7f77-43fc-8296-4d5ddb86e598")]

schema = graphene.Schema(query=Query, types=[Department, Employee, Role])
