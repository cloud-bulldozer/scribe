from . import ScribeBaseClass


class Foo(ScribeBaseClass):
    def __init__(self, path=None):
        ScribeBaseClass.__init__(self, path=path)
