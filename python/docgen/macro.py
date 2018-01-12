import rst_conf
from commandsequence import CommandSequence
from formatter import format_table

class Macro(CommandSequence):
    def __init__(self, name, descr=''):
        CommandSequence.__init__(self, name, descr)
        return

    def format_syntax(self):
        # Add header
        formatted_output = 'Syntax\n' + rst_conf.cs_subhdr_symbol*6 + '\n'

        if not self._name:
            raise ValueError('Macro name is undefined.')
        else:
            formatted_output += '``\\' + self._name

        if self._opts:
            formatted_output += '[options]'

        if self._args:
            for arg in self._args:
                formatted_output += '{' + arg['name'] + '}'

        formatted_output += '``\n'
        return formatted_output + '\n'

    def format_header(self):
        # Add header
        if self._name:
            formatted_output = '.. _' + self._name + ':\n\n'
            formatted_output += (
                '\\\\' + self._name + '\n'
                + rst_conf.cs_hdr_symbol*(len(self._name) + 2) + '\n'
            )
            # Add description
            formatted_output += self._descr + '\n'
        else:
            raise ValueError('Macro name is undefined.')

        return formatted_output + '\n'

    def format_all(self):
        format_string  = self.format_header()
        format_string += self.format_syntax()
        format_string += self.format_opts()
        format_string += self.format_args()

        return format_string
