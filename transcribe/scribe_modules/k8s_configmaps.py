from . import ScribeModuleBaseClass
from . lib.util import format_url

import re as _re
import sys
import json
import re

class K8s_configmaps(ScribeModuleBaseClass):

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
        # No modification is needed to output. Note: some of the configmap
        # data comes in as yaml files. For example see kubelet in stockpile_configmap
        if len(items_full) <= 1:
            print("Error occured in processing k8s ConfigMap data")
            sys.exit(1)
        return items_full
