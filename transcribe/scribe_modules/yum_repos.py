from . import ScribeModuleBaseClass
from . lib.util import format_url


base_url = "http://mirror.centos.org/centos/$releasever/{}/$basearch/"
# object_dict = {}


class Yum_repos(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)
        if input_dict:
            # object_dict['repo_name'] = input_dict['repoid']
            # object_dict['repo_state'] = self.update_repo_state(input_dict)
            # object_dict['base_url'] = format_url(base_url, self.repo_name)
            self.repo_name = input_dict['repoid']
            self.repo_state = self.update_repo_state(input_dict)
            # This is just for the sake of it
            self.base_url = format_url(base_url, self.repo_name)

    def update_repo_state(self, value):
        if value['state'] == 'enabled':
            return 1
        return 0

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
