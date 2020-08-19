import json


def format_url(base_url, key):
    return base_url.format(key)


def dict_to_list(my_dict, *levels):
    dict_list = []
    for lvl in levels:
        if lvl in my_dict:
            my_dict = my_dict[lvl]
        else:
            return dict_list
    for k, v in my_dict.items():
        dict_list.append("%s: %s" % (k, v))
    return dict_list


def validate_length(length, module_name):
    if length <= 1:
        raise ValueError('Error occurred in processing {} data'.format(module_name))
