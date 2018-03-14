import uuid
import json

from pynamodb.attributes import MapAttribute, ListAttribute, UnicodeAttribute, NumberAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model
from werkzeug.security import check_password_hash, generate_password_hash


def is_password_hash(pwhash):
    if pwhash.count('$') < 2:
        return False
    method, salt, hashval = pwhash.split('$', 2)

    return method.startswith('pbkdf2:') and len(method[7:].split(':')) in (1, 2)


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        print 'youuerb'
        if hasattr(obj, 'attribute_values'):
            return obj.attribute_values
        return json.JSONEncoder.default(self, obj)


def json_dumps(obj):
    return json.dumps(obj, cls=ModelEncoder)

class PasswordAttribute(UnicodeAttribute):
    def serialize(self, value):
        if is_password_hash(value):
            return value
        return generate_password_hash(value)

    def deserialize(self, value):
        return value


class SessionMap(MapAttribute):
    id = UnicodeAttribute(null=False)
    start_timestamp = NumberAttribute(null=False)
    end_timestamp = NumberAttribute()
    result = UnicodeAttribute(null=False)


class User(Model, ModelEncoder):
    class Meta:
        table_name = "dunkin"
        host = "https://dynamodb.us-east-1.amazonaws.com"

    def to_dict(self):
        rval = {}
        for key in self.attribute_values:
            rval[key] = self.__getattribute__(key)
        return rval

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
    password = PasswordAttribute(null=False)


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
