import json

keys_stockpile_list = ['stockpile_']
ignore_stockpile_key_list = ['stockpile_user', 'stockpile_output_path']


def check_key_stockpile(key):
    valid_stockpile_check = \
        any(sample_key in key for sample_key in keys_stockpile_list)
    ignore_key_check = not (key in ignore_stockpile_key_list)
    return valid_stockpile_check and ignore_key_check


def load_json(input_json_path):
    with open(input_json_path) as f:
        json_data = json.load(f)
    return json_data
