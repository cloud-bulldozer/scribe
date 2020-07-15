import json

from . import ScribeModuleBaseClass
from . lib.k8s_util import remove_managed_fields 
from transcribe.scribe_modules.lib import util


class K8s_namespaces(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        remove_managed_fields(self._input_dict)
        self._dict['value'] = util.fix_nested_dict(self._input_dict)
        yield self._dict

