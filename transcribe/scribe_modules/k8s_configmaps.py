from . import ScribeModuleBaseClass
from . lib.util import to_list, validate_length

class K8s_configmaps(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        items_full = self._input_dict
        validate_length(len(items_full), self.module)
        # Flatten some of the dictionaries to lists
        items_full = to_list("metadata","annotations",items_full)
        items_full = to_list("metadata","labels",items_full)
        if "data" in items_full.keys():
            # If . in key name replace it with with an _
            for my_key in items_full["data"].keys():
                if "." in my_key:
                    items_full["data"][my_key.replace('.','_')] = items_full["data"].pop(my_key)
            tmp_list = []
            tmp_list.append(items_full["data"])
            items_full["data"] = tmp_list
        output_dict = self._dict
        output_dict['value'] = items_full
        yield output_dict
