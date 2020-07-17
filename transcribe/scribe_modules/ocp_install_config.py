from . import ScribeModuleBaseClass
from . lib.util import format_url

import re as _re
import sys
import json
import re

class Ocp_install_configm(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)
        if input_dict:
            self.value = self._parse(input_dict)

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def _parse(self, items_full):
        item = dict(items_full)
        return item
