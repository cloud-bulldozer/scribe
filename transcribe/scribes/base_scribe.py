from abc import ABCMeta, abstractmethod


class ScribeBaseClass(metaclass=ABCMeta):
    def __init__(self, path=None, source_type=None):
        if source_type:
            self._source_type = source_type
        if path:
            self._path = path
        self._dict = None

    @abstractmethod
    def emit_scribe_dict(self):
        pass
