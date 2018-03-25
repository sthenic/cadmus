import os
import re
from . import rst_conf
from .latex_parser import parse_file
from .formatter import format_table


class File:
    # Locals
    _file = ''
    _dobjects = None

    # Constructor
    def __init__(self, file=''):
        self._dobjects = {
            'macro': [],
            'environment': [],
            'configurable_element': [],
            'document_class': []
        }
        self.set_file(file)
        return

    def set_file(self, file):
        self._file = file
        if self._file:
            self.index_file()
        return

    def index_file(self):
        if not self._file:
            ValueError('File object has no target file.')

        self._dobjects = parse_file(self._file)
        return

    def generate_rst(self, mask, output_dir, rst_conf):
        if not self._file:
            ValueError('File object has no target file.')

        format_string = ''
        # Validate output_dir
        if not os.path.exists(output_dir):
            print('Creating output directory \'' + output_dir +
                  '\' since it does not exist.')
            os.makedirs(output_dir)

        # Extract the package name from the file name
        (package_name, package_type) = os.path.basename(self._file).split('.')

        # The mask is either a string or a list of strings since a few
        # different modes are supported.
        if isinstance(mask, str):
            # The mask is a string
            if (mask == 'all'):
                # Everything parsed from the target file should be output and
                # placed in a single file. The output file name is the package
                # file name.
                for (midx, macro) in enumerate(self._dobjects['macro']):
                    format_string += '----\n\n'
                    format_string += macro.format_all(rst_conf)

                for (midx, env) in enumerate(self._dobjects['environment']):
                    format_string += '----\n\n'
                    format_string += env.format_all(rst_conf)

                print('Generating file \'' + package_name + '_all.rst\'.')
                with open(os.path.join(output_dir, package_name + '_all.rst'),
                          'w') as f:
                    f.write(format_string)

            elif (mask == 'allsplit'):
                # Everything parsed from the target file should be output and
                # each macro should be placed in a different file. The output
                # file name is the macro name.
                for macro in self._dobjects['macro']:
                    format_string = '----\n\n'
                    format_string += macro.format_all(rst_conf)

                    print('Generating file \'' + macro._name + '.rst\'.')
                    with open(os.path.join(output_dir, macro._name + '.rst'),
                              'w') as f:
                        f.write(format_string)

                for env in self._dobjects['environment']:
                    format_string = '----\n\n'
                    format_string += env.format_all(rst_conf)

                    print('Generating file \'' + env._name + '.rst\'.')
                    with open(os.path.join(output_dir, env._name + '.rst'),
                              'w') as f:
                        f.write(format_string)

                if self._dobjects['configurable_element']:
                    header = ['Style element', 'Description', 'Default value']
                    body = []
                    for e in self._dobjects['configurable_element']:
                        body.append(e.format_table_row())
                    table_dict = {'header': header, 'body': body}

                    print('Generating file \'' + package_name + '_cfg.rst\'.')
                    with open(os.path.join(output_dir, package_name
                                                       + '_cfg.rst'),
                              'w') as f:
                        f.write(format_table(table_dict))

                for dc in self._dobjects['document_class']:
                    print('Generating file \'' + dc._name + '_opts.rst\'.')
                    with open(os.path.join(output_dir, dc._name + '_opts.rst'),
                              'w') as f:
                        # Only write option table, without header.
                        f.write(dc.format_opt_table())

            else:
                # The string is assumed to be a regexp used to match the name
                # of one or several macros.
                for macro in self._dobjects['macro']:
                    if re.match(mask, macro._name):
                        with open(os.path.join(output_dir, macro._name
                                                           + '.rst'),
                                  'w') as f:
                            f.write(macro.format_all(rst_conf))

                for env in self._dobjects['environment']:
                    if re.match(mask, env._name):
                        with open(os.path.join(output_dir, env._name + '.rst'),
                                  'w') as f:
                            f.write(env.format_all(rst_conf))

        elif isinstance(mask, list):
            # The mask is a list of strings (hopefully)
            print('You gave me a list but I\'m not implemented yet :(')
        else:
            raise ValueError('Mask is not a string or a list.')

        return
