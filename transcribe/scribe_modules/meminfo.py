from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Meminfo(ScribeModuleBaseClass):

    def parse(self):
        meminfo_lines = self._input_dict.strip().split('\n')
        validate_length(len(meminfo_lines), self.module)
        self._dict["value"] = {}
        for line in meminfo_lines:
            self._dict["value"][line.split(":")[0].strip()] = line.split(":")[1].strip()
        yield self._dict
