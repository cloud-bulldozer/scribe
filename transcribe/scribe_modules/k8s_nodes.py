from . import ScribeModuleBaseClass
from . lib.util import dict_to_list, validate_length


class K8s_nodes(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        node_info = {
            "name": self._input_dict["metadata"]["name"],
            "labels": dict_to_list(self._input_dict, "metadata", "labels"),
            "spec": self._input_dict["spec"],
            "nodeInfo": self._input_dict["status"]["nodeInfo"],
            "addresses": self._input_dict["status"]["addresses"],
            "allocatable": self._input_dict["status"]["allocatable"],
            "capacity": self._input_dict["status"]["capacity"]
        }
        self._dict['value'] = node_info
        yield self._dict
