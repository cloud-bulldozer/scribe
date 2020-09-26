from . import ScribeModuleBaseClass
from . lib.util import format_url

base_url = "http://mirror.centos.org/centos/$releasever/{}/$basearch/"


class Yum_repos(ScribeModuleBaseClass):

    def parse(self):
        output_dict = self._dict
        output_dict['repo_name'] = self._input_dict['repoid']
        output_dict['repo_state'] = 1 if self._input_dict["value"] == "enabled" else 0
        output_dict['base_url'] = format_url(base_url, output_dict['repo_name'])
        yield output_dict
