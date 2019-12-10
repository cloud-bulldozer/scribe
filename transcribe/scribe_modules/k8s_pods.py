from . import ScribeModuleBaseClass

import re as _re
import sys


class K8s_pods(ScribeModuleBaseClass):

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
        def to_list(first_lvl, second_lvl, my_dict):
            if first_lvl in my_dict:
                if second_lvl in my_dict[first_lvl]:
                    new_dict = {}
                    for key,value in my_dict[first_lvl][second_lvl].items():
                        if '.' in key:
                            new_dict[key.replace('.','_')] = value
                    my_dict[first_lvl][second_lvl] = new_dict
                    tmp_list = []
                    tmp_list.append(my_dict[first_lvl][second_lvl])
                    my_dict[first_lvl][second_lvl] = tmp_list
            return my_dict
        # Flatten some of the dictionaries to lists
        if len(items_full) <= 1:
            print("Error occured in processing k8s Pods data")
            sys.exit(1)

        items_full = to_list("metadata","annotations",items_full)
        items_full = to_list("metadata","labels",items_full)
        items_full = to_list("spec","securityContext",items_full)    
        items_full = to_list("spec","nodeSelector",items_full) 

        return items_full
