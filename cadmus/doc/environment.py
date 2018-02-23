from .control_sequence import ControlSequence
from .formatter import format_table

class Environment(ControlSequence):
    def __init__(self, name, descr=''):
        ControlSequence.__init__(self, name, descr)
        return

    def format_syntax(self, rst_conf):
        # Add header
        formatted_output = 'Syntax\n' + rst_conf['cs_subsection_char']*6 + '\n'

        if not self._name:
            raise ValueError('Macro name is undefined.')
        else:
            formatted_output += (
                '.. code-block:: LaTeX\n\n'
                + ' '*rst_conf['cs_tab_size'] + '\\begin{' + self._name + '}'
            )

        if self._opts:
            formatted_output += '[options]'

        if self._kwargs:
            formatted_output += '{kwargs}'

        if self._args:
            for arg in self._args:
                formatted_output += '{' + arg['name'] + '}'
        formatted_output += '\n'

        formatted_output += (
            ' '*rst_conf['cs_tab_size'] + '...\n'
            + ' '*rst_conf['cs_tab_size'] + '\\end{' + self._name + '}\n'
        )

        return formatted_output + '\n'

    def format_header(self, rst_conf):
        if self._name:
            # Insert custom RST role
            formatted_output = ('.. role:: environment(raw)\n' +
                                '    :format: html\n' +
                                '    :class: environment\n\n')
            # Define formatted cross-reference using the RST replacement
            # directive.
            formatted_output += (
                '.. |' + self._name + '_env| replace:: ``' + self._name
                + '`` environment\n'
            )
            # Define cross-reference label
            formatted_output += '.. _' + self._name + '_env:\n\n'
            # Define header
            formatted_output += (
                'Environment :environment:`' + self._name + '`\n'
                + rst_conf['cs_section_char']*(len(self._name) + 27) + '\n'
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
