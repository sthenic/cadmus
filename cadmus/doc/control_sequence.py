from .dobject import DObject
from .formatter import format_table


class ControlSequence(DObject):
    def __init__(self, name, descr=''):
        DObject.__init__(self, name, descr)
        self._opts = []
        self._kwargs = []
        self._args = []
        self.has_opts = False
        self.has_kwargs = False
        self.has_args = False
        return

    def add_option(self, opt, descr, default='N/A'):
        self._opts.append({'name': opt, 'descr': descr, 'default': default})
        return

    def add_keyword_argument(self, kwarg, descr, default='N/A'):
        self._kwargs.append(
            {'name': kwarg, 'descr': descr, 'default': default})
        return

    def add_argument(self, arg, descr):
        self._args.append({'name': arg, 'descr': descr})
        return

    def format_opt_table(self):
        if not self._opts:
            return ''
        # Constuct table dict
        header = ['Option', 'Description', 'Default']
        body = []
        for opt in self._opts:
            body.append(['``' + opt['name'] + '``', opt['descr'],
                         '``' + opt['default'] + '``'])

        return format_table({'header': header, 'body': body})

    def format_opts(self, rst_conf):
        if not self._opts:
            return ''
        formatted_output = (
            # Add label
            '.. _' + self._name + '_opts:\n\n'
            # Add header
            + 'Options\n' + rst_conf['cs_subsection_char']*7 + '\n'
        )

        return formatted_output + self.format_opt_table() + '\n'

    def format_kwarg_table(self):
        if not self._kwargs:
            return ''
        # Constuct table dict
        header = ['Keyword', 'Description', 'Default']
        body = []
        for kwarg in self._kwargs:
            body.append(['``' + kwarg['name'] + '``', kwarg['descr'],
                         '``' + kwarg['default'] + '``'])

        return format_table({'header': header, 'body': body})

    def format_keyword_arguments(self, rst_conf):
        if not self._kwargs:
            return ''
        formatted_output = (
            # Add label
            '.. _' + self._name + '_kwargs:\n\n'
            # Add header
            + 'Keyword Arguments\n' + rst_conf['cs_subsection_char']*17 + '\n'
        )

        return formatted_output + self.format_kwarg_table() + '\n'

    def format_arg_table(self):
        if not self._args:
            return ''
        # Constuct table dict
        header = ['Argument', 'Description']
        body = []
        for arg in self._args:
            body.append(['``' + arg['name'] + '``', arg['descr']])

        return format_table({'header': header, 'body': body})

    def format_args(self, rst_conf):
        if not self._args:
            return ''
        formatted_output = (
            # Add label
            '.. _' + self._name + '_args:\n\n'
            # Add header
            + 'Arguments\n' + rst_conf['cs_subsection_char']*9 + '\n'
        )

        return formatted_output + self.format_arg_table() + '\n'
