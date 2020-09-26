#!/usr/bin/env python3
import json
import sys

from . import scribes
from . import scribe_modules
from . lib.util import validate_document, load_schema_file, check_file


def _create_module_yield_doc(key, value, host_dict, input_type):
    try:
        scribe_module_instance = \
            scribe_modules.create_module(key, input_dict=value,
                                         module_name=key,
                                         host_name=host_dict,
                                         input_type=input_type)
    except (ImportError, ValueError, TypeError) as e:
        print(e)
        return e
    schema = load_schema_file(key)
    try:
        for document in scribe_module_instance.parse():
            output_doc = validate_document(document, schema)
            yield(json.dumps(output_doc, indent=4))
    except (KeyError, ValueError) as e:
        print("Scribe module %s %s error: %s" % (key, type(e).__name__, e), file=sys.stderr)


def transcribe(input_path, scribe_type):
    check_file(input_path)
    scribe_instance = scribes.grab(scribe_type, path=input_path)
    _scribe_dict = scribe_instance.emit_scribe_dict()
    _input_type = scribe_instance._source_type
    for key in sorted(_scribe_dict.keys()):
        for host_dict in _scribe_dict[key]:
            if isinstance(host_dict['value'], list):
                for value in host_dict['value']:
                    yield from _create_module_yield_doc(key, value,
                                                        host_dict['host'],
                                                        _input_type)
            else:
                yield from _create_module_yield_doc(key,
                                                    host_dict['value'],
                                                    host_dict['host'],
                                                    _input_type)
