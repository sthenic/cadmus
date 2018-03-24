from .control_sequence import ControlSequence
from .formatter import format_table

class Macro(ControlSequence):
    def __init__(self, name, descr=''):
        ControlSequence.__init__(self, name, descr)
        # A macro may have options, keyword arguments and arguments.
        self.has_opts   = True
        self.has_kwargs = True
        self.has_args   = True
        return

    def format_syntax(self, rst_conf):
        # Add header
        formatted_output = 'Syntax\n' + rst_conf['cs_subsection_char']*6 + '\n'

        if not self._name:
            raise ValueError('Macro name is undefined.')
        else:
            formatted_output += '``\\' + self._name

        if self._opts:
            formatted_output += '[options]'

        if self._kwargs:
            formatted_output += '{kwargs}'

        if self._args:
            for arg in self._args:
                formatted_output += '{' + arg['name'] + '}'

        formatted_output += '``\n'
        return formatted_output + '\n'

    def format_header(self, rst_conf):
        if self._name:
            # Insert custom RST role
            formatted_output = ('.. role:: macro(raw)\n' +
                                '    :format: html\n' +
                                '    :class: macro\n\n')
            # Define formatted cross-reference using the RST replacement
            # directive.
            formatted_output += (
                '.. |' + self._name + '| replace:: ``\\' + self._name + '``\n'
            )
            # Define cross-reference label
            formatted_output += '.. _' + self._name + ':\n\n'
            # Define header
            formatted_output += (
                ':macro:`\\' + self._name + '`\n'
                + rst_conf['cs_section_char']*(len(self._name) + 10) + '\n'
            )
            # Add description
            formatted_output += self._descr + '\n'
        else:
            raise ValueError('Macro name is undefined.')

        return formatted_output + '\n'

    def format_all(self, rst_conf):
        format_string  = self.format_header(rst_conf)
        format_string += self.format_syntax(rst_conf)
        format_string += self.format_opts(rst_conf)
        format_string += self.format_keyword_arguments(rst_conf)
        format_string += self.format_args(rst_conf)

        return format_string
