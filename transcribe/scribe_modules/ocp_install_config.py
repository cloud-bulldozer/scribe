from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Ocp_install_config(ScribeModuleBaseClass):

    def parse(self):
        validate_length(len(self._input_dict), self.module)
        self._dict['value'] = self._input_dict
        yield self._dict
