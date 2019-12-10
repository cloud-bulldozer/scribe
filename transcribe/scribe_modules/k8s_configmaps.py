from . import ScribeModuleBaseClass
from . lib.util import to_list

import re as _re
import sys
import json
import re

class K8s_configmaps(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)
        if input_dict:
            self.value = self._parse(input_dict)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def _parse(self, items_full):
        # Flatten some of the dictionaries to lists
        if len(items_full) <= 1:
            print("Error occured in processing k8s ConfigMap data")
            sys.exit(1)
         
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

        return items_full
