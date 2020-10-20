import json
from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_net_attachments(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        net_attachment_definition_info = {
            "name": self._input_dict["metadata"]["name"],
            "namespace": self._input_dict["metadata"]["namespace"],
            "config": json.loads(self._input_dict["spec"]["config"])
        }
        self._dict['value'] = net_attachment_definition_info
        yield self._dict
