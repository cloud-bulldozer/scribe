from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Sysctl(ScribeModuleBaseClass):

    def parse(self):
        sysctl_lines = self._input_dict["sysctl"].split("\n")
        validate_length(len(sysctl_lines), self.module)
        for line in sysctl_lines:
            k, v = line.split("=")
            self._dict["entry"] = k.strip()
            self._dict["value"] = v.strip()
            yield self._dict
