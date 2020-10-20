from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_dns(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        ocp_dns = {
            "name": self._input_dict["metadata"]["name"],
            "spec": self._input_dict["spec"]
        }
        self._dict['value'] = ocp_dns
        yield self._dict
