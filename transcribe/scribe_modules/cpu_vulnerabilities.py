import os
from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Cpu_vulnerabilities(ScribeModuleBaseClass):

    def parse(self):
        split_lines = self._input_dict.split('\n')
        validate_length(len(split_lines), self.module)
        cpu_vulnerability = {}
        for line in split_lines:
            fields = line.split(":")
            cpu_vulnerability[os.path.basename(fields[0])] = {}
            cpu_vulnerability[os.path.basename(fields[0])]["status"] = fields[1]
            if len(fields) == 3:
                cpu_vulnerability[os.path.basename(fields[0])]["mitigation"] = fields[2]
        self._dict["value"] = cpu_vulnerability
        yield self._dict
