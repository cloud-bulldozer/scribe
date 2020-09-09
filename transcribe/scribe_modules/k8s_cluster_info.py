from . import ScribeModuleBaseClass
from . lib.util import dict_to_list, validate_length
from . lib.k8s_util import remove_unused_fields


class K8s_cluster_info(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        cluster_info = self._input_dict
        validate_length(len(cluster_info), self.module)
        remove_unused_fields(cluster_info)
        # Flatten some of the dictionaries to lists
        output_dict = self._dict
        output_dict['value'] = cluster_info
        yield output_dict
