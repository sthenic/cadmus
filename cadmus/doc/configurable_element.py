from .dobject import DObject


class ConfigurableElement(DObject):
    def __init__(self, name, descr='', definition=''):
        DObject.__init__(self, name, descr)
        self._definition = definition

    def format_table_row(self):
        table_row = [
            '``\\' + self._name + '``',
            self._descr,
            '``' + self._definition + '``'
        ]
        return table_row
