from . import ScribeModuleBaseClass

import sys

from .lib.util import validate_length


class Lspci(ScribeModuleBaseClass):

    def __init__(self, input_dict=None, module_name=None, host_name=None,
                 input_type=None, scribe_uuid=None):
        ScribeModuleBaseClass.__init__(self, module_name=module_name,
                                       input_dict=input_dict,
                                       host_name=host_name,
                                       input_type=input_type,
                                       scribe_uuid=scribe_uuid)

    def parse(self):
        lspci_data = self._input_dict
        lspci_lines = lspci_data.split('\n\n')

        validate_length(len(lspci_lines), self.module)

        # lspci_lines contains a list of slots and its information.
        # We are yielding a dict of these individual slots.
        for i in range(len(lspci_lines)):
            slot_data = lspci_lines[i].split('\n')
            # sample - ['Slot:\t00:00.0', 'Class:\tHost bridge', 'Vendor:\tIntel Corporation' ..... ]
            self._dict["value"] = {}
            for slot_info in slot_data:
                key = slot_info.split(':\t')[0].strip()
                value = slot_info.split(':\t')[1].strip()
                self._dict["value"][key] = value
            yield self._dict
