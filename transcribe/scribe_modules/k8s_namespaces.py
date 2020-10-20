from . import ScribeModuleBaseClass
from . lib.k8s_util import remove_unused_fields
from . lib.util import dict_to_list


class K8s_namespaces(ScribeModuleBaseClass):

    def parse(self):
        remove_unused_fields(self._input_dict)
        self._input_dict["metadata"]["annotations"] = dict_to_list(self._input_dict,
                                                                   "metadata",
                                                                   "annotations")
        self._input_dict["metadata"]["labels"] = dict_to_list(self._input_dict, "metadata", "labels")
        self._dict['value'] = self._input_dict
        yield self._dict
