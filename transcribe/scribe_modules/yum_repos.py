from . import ScribeModuleBaseClass
from . lib.util import format_url

base_url = "http://mirror.centos.org/centos/$releasever/{}/$basearch/"

class Yum_repos(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        output_dict = self._dict
        output_dict['repo_name'] = self._input_dict['repoid']
        output_dict['repo_state'] = 1 if self._input_dict["value"] == "enabled" else 0
        output_dict['base_url'] = format_url(base_url, output_dict['repo_name'])
        yield output_dict
