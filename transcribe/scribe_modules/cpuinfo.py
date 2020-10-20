from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Cpuinfo(ScribeModuleBaseClass):

    def parse(self):
        output_data = {}
        split_lines = self._input_dict.split('\n')
        validate_length(len(split_lines), self.module)
        for line in split_lines:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "Flags":
                v = v.split(" ")
            output_data[k] = v
        output_dict = self._dict
        output_dict['value'] = output_data
        yield output_dict
