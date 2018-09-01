from . import ScribeBaseClass
from . lib.util import check_key_stockpile
from . lib.util import load_json


class Stockpile(ScribeBaseClass):

    def stockpile_build_initial_dict(self):
        output_dict = {}
        stockpile_data = load_json(self._path)
        for host in stockpile_data:
            for key in stockpile_data[host]:
                temp_value = None
                if check_key_stockpile(key):
                    new_key = key.split('stockpile_')[1]
                    temp_value = stockpile_data[host][key]
                    current_dict = {'host': host, 'value': temp_value}
                    if new_key not in output_dict.keys():
                        output_dict[new_key] = []
                    output_dict[new_key].append(current_dict)
        return output_dict

    def __init__(self, path=None, source_type=None):
        ScribeBaseClass.__init__(self, source_type=source_type, path=path)
        self._dict = self.stockpile_build_initial_dict()

    def emit_scribe_dict(self):
        return self._dict
