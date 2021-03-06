from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_network_operator(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        ocp_network_operator_info = {
            "name": self._input_dict["metadata"]["name"],
            "spec": self._input_dict["spec"],
        }
        self._dict['value'] = ocp_network_operator_info
        yield self._dict
