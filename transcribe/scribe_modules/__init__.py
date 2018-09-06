from importlib import import_module


from . base_scribe_module import ScribeModuleBaseClass ## noqa


def create_module(scribe_module_type, *args, **kwargs):

    try:
        if '.' in scribe_module_type:
            module_name, class_name = scribe_module_type.rsplit('.', 1)
        else:
            module_name = scribe_module_type
            class_name = scribe_module_type.capitalize()

        scribe_module = import_module('transcribe.scribe_modules.' +
                                      module_name, package='scribe_modules')
        scribe_input_class = getattr(scribe_module, class_name)
        instance = scribe_input_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our scribe module \
                          collection!'.format(scribe_module_type))
    else:
        if not issubclass(scribe_input_class, ScribeModuleBaseClass):
            raise ImportError("We currently don't have {}, but you are \
                              welcome to send in the request for \
                              it!".format(scribe_input_class))

    return instance
