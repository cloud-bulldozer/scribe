from . import ScribeModuleBaseClass
from . lib.util import validate_length

import sys
import xmltodict

class Nvidia_smi(ScribeModuleBaseClass):
    
    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        validate_length(len(self._input_dict['xml']), self.module)
        self._dict["value"] = {}
        self._dict["value"] = xmltodict.parse(self._input_dict['xml'])['nvidia_smi_log']
        yield self._dict
