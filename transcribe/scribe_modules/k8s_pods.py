from . import ScribeModuleBaseClass
from . lib.util import dict_to_list, validate_length
from . lib.k8s_util import remove_unused_fields


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
        validate_length(len(items_full), self.module)
        remove_unused_fields(items_full)
        # Flatten some of the dictionaries to lists
        items_full["metadata"]["annotations"] = dict_to_list(items_full, "metadata", "annotations")
        items_full["metadata"]["labels"] = dict_to_list(items_full, "metadata", "labels")
        items_full["spec"]["nodeSelector"] = dict_to_list(items_full, "spec", "nodeSelector")
        output_dict = self._dict
        output_dict['value'] = items_full
        yield output_dict
