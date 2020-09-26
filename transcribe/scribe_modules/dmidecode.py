import re
from . import ScribeModuleBaseClass
from . lib.util import validate_length


class Dmidecode(ScribeModuleBaseClass):

    def parse(self):
        dmide_fullinput = self._input_dict
        output_dict = self._dict
        output_data = {}
        # in case of output such as
        #   BIOS Information
        #      Vendor: LENOVO
        #      ROM Size: 16 MB
        #      Characteristics:
        #           PCI is supported
        # 	        PNP is supported
        #    	    BIOS is upgradeable
        # The values for Characteristics can't be made into a key: val easily,
        # Thus instead of Characteristics being a list, It's now a simple str
        # This is what the next line does
        dmide_fullinput = dmide_fullinput.replace('\n\t\t', ' ')
        split_output = dmide_fullinput.replace('\t', '').split('\n\n')
        validate_length(len(split_output), self.module)
        for record in split_output:
            split_lines = record.split('\n')
            for x in range(len(split_lines)):
                # There are cases where the value has leading whitespaces
                # And also removing multiple whitespaces in general
                split_lines[x] = re.sub(r":\s\s+", ": ", split_lines[x])
                split_lines[x] = re.sub(r"\s\s+", "", split_lines[x])
            if split_lines[0] != "" and len(split_lines) >= 2:
                # Dealing with keys having whitespaces
                split_lines[0] = split_lines[0].replace(' ', '_')
                if split_lines[0] not in output_data:
                    output_data[split_lines[0]] = []
                current_dict = {}
                # splitting only on 1st occurence of ':' as it can be like
                # example
                #     String 1: PSF:
                #     String 2: Product ID: 670635-S01
                for s in split_lines[1:]:
                    if ': ' in s:
                        key_val = s.split(': ', 1)
                    else:
                        continue
                    if len(key_val) <= 1:
                        key_val.append("None")
                    current_dict[key_val[0].replace(' ', '_')] = key_val[1]
                output_data[split_lines[0]].append(current_dict)
        output_dict['value'] = output_data
        yield output_dict
