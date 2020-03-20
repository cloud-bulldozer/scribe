from . import ScribeModuleBaseClass


class Sysctl(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)


    def parse(self):
        for line in self._input_dict["sysctl"].split("\n"):
            k, v = line.split("=")
            self._dict["entry"] = k.strip()
            self._dict["value"] = v.strip()
            yield self._dict
