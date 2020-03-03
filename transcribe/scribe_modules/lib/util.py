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
