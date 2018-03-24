from .dobject import DObject
from .formatter import format_table

class ControlSequence(DObject):
    def __init__(self, name, descr=''):
        DObject.__init__(self, name, descr)
        self._opts      = []
        self._kwargs    = []
        self._args      = []
        self.has_opts   = False
        self.has_kwargs = False
        self.has_args   = False
        return

    def add_option(self, opt, descr, default='N/A'):
        self._opts.append({'name': opt, 'descr': descr, 'default': default})
        return

    def add_keyword_argument(self, kwarg, descr, default='N/A'):
        self._kwargs.append({'name': kwarg, 'descr': descr, 'default': default})
        return

    def add_argument(self, arg, descr):
        self._args.append({'name': arg, 'descr': descr})
        return

    def format_opts(self, rst_conf):
        if not self._opts:
            return ''
        # Add label
        formatted_output = '.. _' + self._name + '_opts:\n\n'
        # Add header
        formatted_output += \
            'Options\n' + rst_conf['cs_subsection_char']*7 + '\n'
        # Constuct table dict
        header = ['Option', 'Description', 'Default']
        body   = []
        for opt in self._opts:
            body.append([
                '``' + opt['name'] + '``',
                opt['descr'],
                '``' + opt['default'] + '``'
            ])
        table_dict = {'header': header, 'body': body}
        # Get formatted output
        formatted_output += format_table(table_dict)

        return formatted_output + '\n'

    def format_keyword_arguments(self, rst_conf):
        if not self._kwargs:
            return ''
        # Add label
        formatted_output = '.. _' + self._name + '_kwargs:\n\n'
        # Add header
        formatted_output += \
            'Keyword Arguments\n' + rst_conf['cs_subsection_char']*17 + '\n'
        # Constuct table dict
        header = ['Keyword', 'Description', 'Default']
        body   = []
        for kwarg in self._kwargs:
            body.append([
                '``' + kwarg['name'] + '``',
                kwarg['descr'],
                '``' + kwarg['default'] + '``'
            ])
        table_dict = {'header': header, 'body': body}
        # Get formatted output
        formatted_output += format_table(table_dict)

        return formatted_output + '\n'

    def format_args(self, rst_conf):
        if not self._args:
            return ''
        # Add label
        formatted_output = '.. _' + self._name + '_args:\n\n'
        # Add header
        formatted_output += \
            'Arguments\n' + rst_conf['cs_subsection_char']*9 + '\n'
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
