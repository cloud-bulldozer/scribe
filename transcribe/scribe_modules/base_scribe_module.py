from abc import ABCMeta, abstractmethod  ## noqa


class ScribeModuleBaseClass(metaclass=ABCMeta):
    # we can do something like this:
    # def __init__(self, dictionary):
    #     for k, v in dictionary.items():
    #         setattr(self, k, v)
    # if we are sure that there's no transformation needed on the
    # input dict.

    def __init__(self, input_dict=None, module_name=None, input_type=None,
                 host_name=None, scribe_uuid=None):
        if module_name:
            self.module = module_name
        self.source_type = input_type
        self.host = host_name
        self.scribe_uuid = scribe_uuid
        # self.value = list(input_dict.values())[0]

    # Ideally we'd be using abstractmethod
    # however since we dont want children classes to write their
    # own methods, we'll be not be using it
    # This also allows users to implement their own __iter__ function
    # in their classes where they can make the object's entities iterable
    # as they please
    # @abstractmethod
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value
