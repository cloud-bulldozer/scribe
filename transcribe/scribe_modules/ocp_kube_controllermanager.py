from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_kube_controllermanager(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        kube_controllermanager_info = {
            "name": self._input_dict["metadata"]["name"],
            "spec": self._input_dict["spec"]
        }
        self._dict['value'] = kube_controllermanager_info
        yield self._dict
