class DObject:
    def __init__(self, name, descr=''):
        self._name    = name
        self._descr   = descr
        self.has_opts = False
        self.has_args = False
        return

    def set_name(self, name):
        self._name = name
        return

    def set_description(self, descr):
        self._descr = descr
        return
