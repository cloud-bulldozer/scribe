from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_default_ingress_controller(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        ocp_default_ingress_controller = {
            "name": self._input_dict["metadata"]["name"],
            "spec": self._input_dict["spec"]
        }
        self._dict['value'] = ocp_default_ingress_controller
        yield self._dict
