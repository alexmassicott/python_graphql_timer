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

    id = UnicodeAttribute(attr_name='id')
    start_timestamp = NumberAttribute(attr_name='start_timestamp')
    end_timestamp = NumberAttribute(attr_name='end_timestamp')
    result = UnicodeAttribute(attr_name='result')

def _get_value_for_deserialize(value):
    key = next(iter(value.keys()))
    if key == NULL:
        return None
    return value[key]

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
    history = ListAttribute(of=SessionMap)
    sessions = NumberAttribute(null=False)
    completions = NumberAttribute(null=False)


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
