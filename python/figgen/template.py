import os
import re

class Template:
    # Locals
    _template = None
    _file     = None # Every element is a line in the file
    _markers  = None # A dict of line indices, i.e. where to place certain
                     # types of content. Updated when content is added.

    # Constructor
    def __init__(self, template):
        self._file    = []
        self._markers = {}
        self.parse_template(template)
        return

    def parse_template(self, template):
        # Validate template
        if not os.path.exists(template):
            raise ValueError('Invalid template specified: ' + template + '.')

        self._template  = template

        files_to_insert = []
        file_id         = 0

        # TODO: Check for OSError?
        with open(template) as f:
            for line in f:
                # Strip the line of leading whitespace
                line = line.lstrip() # TODO: Why error?!
                if line.startswith('%!'):
                    # Line with special comment, find the token.
                    line = line.strip('%!')
                    # Check line for @-token
                    # Group 1: @-token stripped of the @ character
                    # Group 2: First non-whitespace sequence of characters,
                    #          i.e. the argument (optional).
                    match = re.search('\s@insert(\S+)\s+(\S+)?.*$', line)
                    if match:
                        token = match.group(1)
                        if token == 'file':
                            file_path = match.group(2)
                            if not file_path:
                                raise ValueError(
                                    'Missing argument to @insertfile in ' +
                                    'file \'' + template + '\'.'
                                )
                            # If the path is not an absolute path, assume
                            # relative to the template directory.
                            if not os.path.isabs(file_path):
                                file_path = os.path.abspath(os.path.join(
                                    os.path.dirname(template),
                                    file_path
                                ))
                            # Check if the file exists
                            if not os.path.exists(file_path):
                                raise ValueError(
                                    'Argument to @insertfile in file\'' +
                                    template + '\' does not exist.'
                                )
                            # Append path to list of files to insert
                            files_to_insert.append(file_path)
                            self._markers['file' + str(file_id)] = \
                                len(self._file)
                            file_id += 1
                        else:
                            # Remember where to insert the content type
                            # indicated by the token.
                            self._markers[token] = len(self._file)
                            # Append a dummy line to the file to resolve
                            # content type tokens next to each other.
                            self._file.append('')
                    else:
                        # TODO: Maybe silently continue?
                        raise ValueError('Special comment without @-token.')
                else:
                    # Regular line, add to the file
                    self._file.append(line)

        # Insert files
        for (file_id, file_path) in enumerate(files_to_insert):
            # File existence is guaranteed
            with open(file_path) as f:
                for line in f:
                    self.insert_content(line, 'file' + str(file_id))

        return

    def insert_content(self, content, content_type):
        if content_type in self._markers:
            # Find insertion point in file
            ins_idx = self._markers[content_type]
            # Insert contents
            self._file.insert(ins_idx, content)
            # Increment markers with index higher or equal to the current
            # content marker
            for (content_type, idx) in self._markers.items():
                if (idx >= ins_idx):
                    self._markers[content_type] += 1
        else:
            raise ValueError(
                'No marker for content type ' + content_type + ' found.')

    def write_file(self, output_path):
        dirname = os.path.dirname(output_path)
        if not os.path.exists(dirname):
            print('Creating directory ' + dirname + '.')
            os.makedirs(dirname)

        with open(output_path, 'w') as f:
            print(
                'Writing file \'' + output_path + '\' using template \'' + \
                 self._template + '\'.')

            f.write(''.join(self._file))

        return
