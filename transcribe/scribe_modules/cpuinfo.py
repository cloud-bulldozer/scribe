from . import ScribeModuleBaseClass
from . lib.util import validate_length

import re as _re

class Cpuinfo(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        cpu_fullinput = self._input_dict
        output_data = {}
        split_lines = cpu_fullinput.get("lscpu").split('\n')
        validate_length(len(split_lines), self.module)
        for l in split_lines:
            k, v = l.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "Flags":
                v = v.split(" ")
            output_data[k] = v
        output_dict = self._dict
        output_dict['value'] = output_data
        yield output_dict
