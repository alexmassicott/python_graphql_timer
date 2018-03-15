import uuid
import json

from pynamodb.attributes import MapAttribute, ListAttribute, UnicodeAttribute, NumberAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model
from pynamodb.constants import NULL
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'attribute_values'):
            return obj.attribute_values
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
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
    def deserialize(self, values):
        deserialized_dict = dict()
        for k in values:
            v = values[k]
            attr_value = _get_value_for_deserialize(v)
            key = self._dynamo_to_python_attr(k)
            attr_class = self._get_deserialize_class(key, v)
            if attr_class is None:
                continue
            deserialized_value = None
            if attr_value is not None:
                deserialized_value = attr_class.deserialize(attr_value)

            deserialized_dict[key] = json.dumps(deserialized_value)

        # If this is a subclass of a MapAttribute (i.e typed), instantiate an instance
        return deserialized_dict

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
    password = PasswordAttribute(null=False)


if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
