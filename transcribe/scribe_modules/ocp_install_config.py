from . import ScribeModuleBaseClass
from . lib.util import dict_to_list
from . lib.k8s_util import remove_unused_fields


class Ocp_install_config(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        remove_unused_fields(self._input_dict)
        self._input_dict["metadata"]["annotations"] = dict_to_list(self._input_dict, "metadata", "annotations")
        self._input_dict["metadata"]["labels"] = dict_to_list(self._input_dict, "metadata", "labels")
        self._dict['value'] = self._input_dict
        yield self._dict
