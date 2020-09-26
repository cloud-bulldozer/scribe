from . import ScribeModuleBaseClass
from . lib.util import validate_length


class K8s_cluster_info(ScribeModuleBaseClass):

    def parse(self):
        cluster_info = self._input_dict
        validate_length(len(cluster_info), self.module)
        self._dict['value'] = cluster_info
        yield self._dict
