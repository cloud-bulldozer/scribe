import sys
from . import ScribeModuleBaseClass


class Meminfo(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)


    def parse(self):
        meminfo_lines = self._input_dict["meminfo"].strip().split('\n')
        self._dict["value"] = {}
        for l in meminfo_lines:
            self._dict["value"][l.split(":")[0].strip()] = l.split(":")[1].strip()
        yield self._dict
