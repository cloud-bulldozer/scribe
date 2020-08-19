from . import ScribeModuleBaseClass
from . lib.util import dict_to_list, validate_length
from . lib.k8s_util import remove_unused_fields


class K8s_nodes(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        nodes_full = self._input_dict
        validate_length(len(nodes_full), self.module)
        remove_unused_fields(nodes_full)
        # Flatten some of the dictionaries to lists
        nodes_full["metadata"]["annotations"] = dict_to_list(nodes_full, "metadata", "annotations")
        nodes_full["metadata"]["labels"] = dict_to_list(nodes_full, "metadata", "labels")
        output_dict = self._dict
        output_dict['value'] = nodes_full
        yield output_dict
