#!/usr/bin/env python3
import json
import uuid


from . import scribes
from . import scribe_modules
from . lib.util import validate_document, load_schema_file, check_file


def transcribe(input_path, scribe_type):
    check_file(input_path)
    scribe_instance = scribes.grab(scribe_type, path=input_path)
    _scribe_dict = scribe_instance.emit_scribe_dict()
    _input_type = scribe_instance._source_type
    _scribe_uuid = str(uuid.uuid4())
    # print(json.dumps(scribe_dict,indent=4))
    for key in sorted(_scribe_dict.keys()):
        for host_dict in _scribe_dict[key]:
            if isinstance(host_dict['value'], list):
                for value in host_dict['value']:
                    try:
                        scribe_module_instace = \
                            scribe_modules.create_module(key, input_dict=value,
                                                         module_name=key,
                                                         host_name=host_dict['host'], ## noqa
                                                         input_type=_input_type,  ## noqa
                                                         scribe_uuid=_scribe_uuid)  ## noqa
                    except ImportError as e:
                        print(e)
                        continue
                    schema = load_schema_file(key)
                    try:
                        output_doc = \
                            validate_document(dict(scribe_module_instace),
                                              schema)
                    except ValueError as e:
                        print(e)
                        continue
                    yield(json.dumps(output_doc, indent=4))
            else:
                try:
                    scribe_module_instace = \
                        scribe_modules.create_module(key,
                                                     input_dict=host_dict['value'], ## noqa
                                                     module_name=key,
                                                     host_name=host_dict['host'], ## noqa
                                                     input_type=_input_type,
                                                     scribe_uuid=_scribe_uuid)
                except ImportError as e:
                    print(e)
                    continue
                schema = load_schema_file(key)
                try:
                    output_doc = \
                        validate_document(dict(scribe_module_instace),
                                          schema)
                except ValueError as e:
                    print(e)
                    continue
                yield(json.dumps(output_doc, indent=4))
