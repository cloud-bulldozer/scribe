from . import ScribeModuleBaseClass
from . lib.util import to_list, validate_length

import json


class K8s_namespaces(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        items_full = self._input_dict
        # To help with nested dictionaries that are in a format with
        # escape characters we need to clean it up
        new_items = json.dumps(items_full)
        new_items = new_items.replace('\\n',"")
        new_items = new_items.replace('\\'," ")
        new_items = new_items.replace(" \"","\"")
        new_items = new_items.replace(":\"{",": {")
        new_items = new_items.replace("}\"}","}}")
        new_items = new_items.replace("}}\"","}}")
        validate_length(len(new_items), self.module)
        # Flatten some of the dictionaries to lists
        new_dict = json.loads(new_items)
        new_dict = to_list("metadata","annotations",new_dict)
        new_dict = to_list("metadata","labels",new_dict)
        output_dict = self._dict
        output_dict['value'] = new_dict
        yield output_dict
