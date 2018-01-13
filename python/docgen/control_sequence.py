import rst_conf
from dobject import DObject
from formatter import format_table

class ControlSequence(DObject):
    def __init__(self, name, descr=''):
        DObject.__init__(self, name, descr)
        self._opts    = []
        self._args    = []
        self.has_opts = True
        self.has_args = True
        return

    def add_option(self, opt, descr, default='N/A'):
        self._opts.append({'name': opt, 'descr': descr, 'default': default})
        return

    def add_argument(self, arg, descr):
        self._args.append({'name': arg, 'descr': descr})
        return

    def format_opts(self):
        if not self._opts:
            return ''
        # Add header
        formatted_output = 'Options\n' + rst_conf.cs_subhdr_symbol*7 + '\n'
        # Constuct table dict
        header = ['Option', 'Description', 'Default']
        body   = []
        for opt in self._opts:
            body.append([
                '``' + opt['name'] + '``',
                opt['descr'],
                opt['default']
            ])
        table_dict = {'header': header, 'body': body}
        # Get formatted output
        formatted_output += format_table(table_dict)

        return formatted_output + '\n'

    def format_args(self):
        if not self._args:
            return ''
        # Add header
        formatted_output = 'Arguments\n' + rst_conf.cs_subhdr_symbol*9 + '\n'
        # Constuct table dict
        header = ['Argument', 'Description']
        body   = []
        for arg in self._args:
            body.append([
                '``' + arg['name'] + '``',
                arg['descr']
            ])
        table_dict = {'header': header, 'body': body}
        # Get formatted output
        formatted_output += format_table(table_dict)

        return formatted_output + '\n'
