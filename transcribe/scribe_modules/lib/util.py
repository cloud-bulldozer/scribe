import json

def format_url(base_url, key):
    return base_url.format(key)

# Currently this function takes two specific levels
# of depth. However it probably should be expanded
# to allow for any depth
def to_list(first_lvl, second_lvl, my_dict):
    if first_lvl in my_dict:
        if second_lvl in my_dict[first_lvl]:
            tmp_list = []
            tmp_list.append(my_dict[first_lvl][second_lvl])
            my_dict[first_lvl][second_lvl] = tmp_list
    return my_dict


def validate_length(length, module_name):
    if length <= 1:
        raise ValueError('Error occurred in processing {} data'.format(module_name))


def fix_nested_dict(input_dict):
    # To help with nested dictionaries that are in a format with
    # escape characters we need to clean it up
    new_items = json.dumps(input_dict)
    new_items = new_items.replace('\\n',"")
    new_items = new_items.replace('\\',"")
    new_items = new_items.replace(" \"","\"")
    new_items = new_items.replace(":\"{",": {")
    new_items = new_items.replace("}\"}","}}")
    new_items = new_items.replace("}}\"","}}")
    # Flatten some of the dictionaries to lists
    new_dict = json.loads(new_items)
    new_dict = to_list("metadata","annotations", new_dict)
    new_dict = to_list("metadata","labels", new_dict)
    return new_dict
