from . import ScribeModuleBaseClass
from .lib.util import validate_length


class Lspci(ScribeModuleBaseClass):

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
