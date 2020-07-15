from . import ScribeModuleBaseClass
from . lib.util import validate_length
from . lib.k8s_util import remove_managed_fields

class K8s_pods(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        items_full = self._input_dict
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
        validate_length(len(items_full), self.module)
        # Flatten some of the dictionaries to lists
        items_full = to_list("metadata","annotations",items_full)
        items_full = to_list("metadata","labels",items_full)
        items_full = to_list("spec","securityContext",items_full)
        items_full = to_list("spec","nodeSelector",items_full)
        remove_managed_fields(items_full)
        output_dict = self._dict
        output_dict['value'] = items_full
        yield output_dict
