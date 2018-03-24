from .control_sequence import ControlSequence
from .formatter import format_table

class DocumentClass(ControlSequence):
    def __init__(self, name, descr=''):
        ControlSequence.__init__(self, name, descr)
        # A document class may have options.
        self.has_opts   = True
        return
