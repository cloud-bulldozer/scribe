from . import ScribeModuleBaseClass
from . lib.util import validate_length, dict_to_list

import sys
import xmltodict
from collections import OrderedDict

class Nvidia_smi(ScribeModuleBaseClass):
    
    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        validate_length(len(self._input_dict['xml']), self.module)
        self._dict["value"] = {}
        self._dict["value"] = xmltodict.parse(self._input_dict['xml'])['nvidia_smi_log']
        
        keys_to_toss = ["fan_speed", \
                        "performance_state", \
                        "clocks_throttle_reasons", \
                        "fb_memory_usage", \
                        "bar1_memory_usage", \
                        "compute_mode", \
                        "utilization", \
                        "encoder_stats", \
                        "fbc_stats", \
                        "ecc_mode", \
                        "ecc_errors", \
                        "retired_pages", \
                        "remapped_rows", \
                        "temperature", \
                        "power_readings", \
                        "clocks", \
                        "applications_clocks", \
                        "default_applications_clocks", \
                        "max_clocks", \
                        "max_customer_boost_clocks", \
                        "clock_policy", \
                        "supported_clocks", \
                        "processes", \
                        "accounted_processes"]

        temp_list = []
        if "gpu" in self._dict["value"]:
            for gpu_dict in self._dict["value"]["gpu"]:
                keep = keys_to_toss ^ gpu_dict.keys()
                temp_list.append(dict((key, gpu_dict[key]) for key in keep))
            
            temp_list = [OrderedDict(sorted(i.items())) for i in temp_list]
            self._dict["value"]["gpu"] = temp_list
            self._dict["value"]["gpu"] = [dict_to_list(i) for i in self._dict["value"]["gpu"]]
        
        yield self._dict
