import pkg_resources
import sys
import yaml
from cerberus import Validator
from pathlib import Path


schema_path_parent = 'transcribe/schema/{}.yml'


def build_default_scribe_keys(input_dict):
    return list({j for i in input_dict.values() for j in i})


def check_file(input_data_path):
    input_file_object = Path(input_data_path)
    if not input_file_object.is_file():
        print("Exiting: file in path {} doesnt exist".format(input_data_path))
        sys.exit(1)


def load_schema_file(key):
    schema_path = schema_path_parent.format(key)
    schema_path_key = pkg_resources.resource_filename('scribe', schema_path)
    return yaml.load(open(schema_path_key))


def validate_document(input_dict, input_schema):
    validator_instance = Validator()
    status = validator_instance.validate(input_dict, input_schema)
    if not status:
        raise ValueError(validator_instance.errors)
    else:
        return validator_instance.document
