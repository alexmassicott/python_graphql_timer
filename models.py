import uuid
import json

from pynamodb.attributes import MapAttribute, ListAttribute, UnicodeAttribute, NumberAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model
from pynamodb.constants import NULL
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash


class Session(Model):
    class Meta:
        table_name = "sessions"
        host = "https://dynamodb.us-east-1.amazonaws.com"

    id = UnicodeAttribute(hash_key=True)
    start_timestamp = NumberAttribute(null=False)
    end_timestamp = NumberAttribute(null=False)
    result = UnicodeAttribute()



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
    email = UnicodeAttribute(null=False)
    sessions = NumberAttribute(null=False)
    completions = NumberAttribute(null=False)


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
