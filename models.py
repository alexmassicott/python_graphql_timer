import uuid
import json

from graphene_pynamodb.relationships import OneToOne
from pynamodb.attributes import MapAttribute, ListAttribute, UnicodeAttribute, NumberAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model
from pynamodb.constants import NULL
from flask import jsonify


class IdIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()
        index_name = 'uid-index'
        read_capacity_units = 1
        write_capacity_units = 1

    uid = UnicodeAttribute(hash_key=True)


class User(Model):
    class Meta:
        table_name = "dunkin"
        host = "https://dynamodb.us-east-1.amazonaws.com"

    def __init__(self, hash_key=None, range_key=None, **args):
        Model.__init__(self, hash_key, range_key, **args)
        if not self.id:
            self.id = str(uuid.uuid4())

    id = UnicodeAttribute(hash_key=True)
    role = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    picture = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=False)
    sessions = NumberAttribute(null=True)
    completions = NumberAttribute(null=True)
    last_login = NumberAttribute(null=False)


class Session(Model):
    class Meta:
        table_name = "sessions"
        host = "https://dynamodb.us-east-1.amazonaws.com"

    sid = UnicodeAttribute(hash_key=True)
    uid = OneToOne(User)
    time = NumberAttribute(null=True)
    start_timestamp = NumberAttribute(range_key=True)
    end_timestamp = NumberAttribute(null=True)
    result = UnicodeAttribute()

class SessionIdIndex(Model):
    class Meta:
        table_name = "sessions"
        host = "https://dynamodb.us-east-1.amazonaws.com"

    sid = UnicodeAttribute(hash_key=True)
    uid = UnicodeAttribute()
    id_index = IdIndex()
    time = NumberAttribute(null=True)
    start_timestamp = NumberAttribute(range_key=True)
    end_timestamp = NumberAttribute(null=True)
    result = UnicodeAttribute()
