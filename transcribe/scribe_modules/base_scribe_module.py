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
        self._dict = dict(module=self.module, host=self.host,
                          source_type=self.source_type,
                          scribe_uuid=self.scribe_uuid)
        if input_dict:
            self._input_dict = input_dict
        else:
            raise ValueError('Input dictionary is empty for module %s' % module_name)

    @abstractmethod
    def parse(self):
        pass
