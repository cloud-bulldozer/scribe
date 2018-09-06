from importlib import import_module


from . base_scribe import ScribeBaseClass ## noqa


def grab(scribe_input_type, *args, **kwargs):

    try:
        if '.' in scribe_input_type:
            module_name, class_name = scribe_input_type.rsplit('.', 1)
        else:
            module_name = scribe_input_type
            class_name = scribe_input_type.capitalize()

        scribe_module = import_module('transcribe.scribes.' + module_name,
                                      package='scribes')
        scribe_input_class = getattr(scribe_module, class_name)
        instance = scribe_input_class(*args, **kwargs,
                                      source_type=scribe_input_type)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our \
                          scribe collection!'.format(scribe_input_type))
    # else:
    #     if not issubclass(scribe_input_class, ScribeBaseClass):
    #         raise ImportError("We currently don't have {}, but you are \
    #                             welcome to send in the request for \
    #                             it!".format(scribe_input_class))

    return instance
