from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_kube_apiserver(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        kube_apiserver_info = {
            "name": self._input_dict["metadata"]["name"],
            "spec": self._input_dict["spec"]
        }
        self._dict['value'] = kube_apiserver_info
        yield self._dict
