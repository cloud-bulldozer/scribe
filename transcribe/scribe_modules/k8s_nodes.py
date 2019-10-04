from . import ScribeModuleBaseClass
from . lib.util import format_url

import re as _re
import sys


class K8s_nodes(ScribeModuleBaseClass):

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

    def _parse(self, nodes_full):
        # Currently no work needs to be done to node info so we
        # just confirm that it has data and move on
        if len(nodes_full) <= 1:
            print("Error occured in processing k8s Nodes data")
            sys.exit(1)
        return nodes_full
