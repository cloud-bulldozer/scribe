from . import ScribeModuleBaseClass
from . lib.util import dict_to_list, validate_length
from . lib.k8s_util import remove_unused_fields


class K8s_configmaps(ScribeModuleBaseClass):

    def parse(self):
        items_full = self._input_dict
        validate_length(len(items_full), self.module)
        # Flatten some of the dictionaries to lists
        remove_unused_fields(items_full)
        items_full["metadata"]["annotations"] = dict_to_list(items_full, "metadata", "annotations")
        items_full["metadata"]["labels"] = dict_to_list(items_full, "metadata", "labels")
        if "data" in items_full.keys():
            items_full["data"] = str(items_full["data"])
        output_dict = self._dict
        output_dict['value'] = items_full
        yield output_dict
