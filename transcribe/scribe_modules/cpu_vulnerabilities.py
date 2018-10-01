from . import ScribeModuleBaseClass
from . lib.util import format_url


class Cpu_vulnerabilities(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)
        if input_dict:
            self._assign_properties(self._parse(input_dict))


    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def _assign_properties(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

    def _parse(self, input_parse):
        output_dict = {}
        if '/' in input_parse:
            input_string = input_parse.split('/')[-1]
        else:
            input_string = input_parse
        if ':' in input_string:
            name_string = input_string.split(':')
            output_dict['vulnerability_name'] = name_string[0]
            if 'Vulnerable' in input_string:
                output_dict['current_vulnerability_status'] = True
                vulnerable_string = input_string.split('Vulnerable: ')
                if len(vulnerable_string) >= 2:
                    output_dict['current_vulnerability_type'] = \
                        vulnerable_string[1]
            else:
                output_dict['current_vulnerability_status'] = False
            if 'Mitigation' in input_string:
                output_dict['mitigation_exists'] = True
                mitigation_string = input_string.split('Mitigation: ')
                if len(mitigation_string) >= 2:
                    output_dict['mitigation_type'] = \
                        mitigation_string[1]
            else:
                output_dict['mitigation_exists'] = False
        return output_dict
