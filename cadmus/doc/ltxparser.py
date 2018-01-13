# Description:
#   This module implements functions able to parse files written in LaTeX,
#   extract docstrings and match them to the supported objects, e.g. macros.
from enum import Enum
from .macro import Macro
from .environment import Environment
from .configurable_element import ConfigurableElement
import os
import re

# TODO Investigate use of a dict to compound variables used during different
# parser states.

regex = {
    'newcommand'     : '\s*\\\\newcommand\s*(.*)$',
    'newenvironment' : '\s*\\\\newenvironment\s*(.*)$'
}

def parse_file(file_path):
    """This function parses the target file and combines the docstrings with
       their respective document object.

    Args:
      file_path (string): The path to the target file

    Returns:
      dobjects: A dict of document objects
    """
    # Local document object dict
    dobjects = {
        'macro'                : [],
        'environment'          : [],
        'configurable_element' : []
    }

    # Parser states as an enum
    class State(Enum):
        IDLE       = 0
        CS_DESCR   = 1
        CS_OPT     = 2
        CS_ARG     = 3
        NAME       = 4
        DOBJ_DONE  = 5
        CFG_DESCR  = 6
        CFG_NAME   = 7
        CFG_DEF    = 8

    # Information containers. Different document objects may support a
    # different combination of information containers.
    opts         = []
    args         = []
    descr        = ''
    cfg_def      = ''
    name         = ''
    state        = State.IDLE
    dobject_type = ''
    is_newline   = True
    is_valid     = False

    # Validate file
    if not os.path.exists(file_path):
        raise ValueError('Attempted file parsing without a valid file.')

    with open(file_path) as f:
        for line in f:
            # Strip the line of leading and trailing whitespace
            line = line.strip()
            if line.startswith('%!'):
                # Strip the special comment token
                line = line.lstrip('%!')
                # Check line for @-token
                # Group 1: @-token stripped of the @ character
                # Group 4: Token argument (valid for certain tokens)
                # Group 6: Token default value (valid for certain tokens)
                # Group 8: Token text, needs to be combined with group 4 for
                #          tokens which do not have an argument.
                match = re.search('\s*@(\S+)'
                                  '(\s+((\S+?)(::(.+)::)?)(\s|$))?'
                                  '\s*(.*)$', line)
                if match:
                    # Found a @-token
                    token = match.group(1)
                    if token == 'descr':
                        descr = ''
                        if match.group(4):
                            descr = match.group(4)
                        if match.group(8):
                            descr += ' ' + match.group(8)
                        is_newline = not descr
                        state      = State.CS_DESCR

                    elif token == 'opt':
                        # Validate argument
                        if not match.group(4):
                            raise ValueError('Missing argument to token {}.'
                                             .format(token))

                        opts.append({'name': match.group(4),
                                     'descr': match.group(8)})

                        if match.group(5):
                            opts[-1]['default'] = match.group(6)

                        state = State.CS_OPT

                    elif token == 'arg':
                        # Validate argument
                        if not match.group(4):
                            raise ValueError('Missing argument to token {}.'
                                             .format(token))

                        args.append({'name': match.group(4),
                                     'descr': match.group(8)})

                        state = State.CS_ARG

                    elif token == 'cfg':
                        descr = ''
                        if match.group(4):
                            descr = match.group(4)
                        if match.group(8):
                            descr += ' ' + match.group(8)
                        state = State.CFG_DESCR

                    else:
                        # Perhaps allow this error? Quietly carry on?
                        raise ValueError('Unknown token ' + token + '.')

                    # If this line is reached, the internal variables are no
                    # longer empty.
                    is_valid = True
                else:
                    # Special comment line without @-token, check state and
                    # append to the description of the token under
                    # construction. Text is ignored if state is IDLE.
                    if state == State.CS_DESCR:
                        if not line:
                            # Empty line intended by the author
                            descr += '\n\n'
                            is_newline = True
                        else:
                            # Prepend a space unless first line in a section.
                            descr += ' '*(not is_newline) + line.strip()
                            if is_newline:
                                is_newline = False

                    elif state == State.CS_OPT:
                        opts[-1]['descr'] += ' ' + line.strip()

                    elif state == State.CS_ARG:
                        args[-1]['descr'] += ' ' + line.strip()

                    elif state == State.CFG_DESCR:
                        descr += ' ' + line.strip()

            elif state == State.NAME:
                # A \newcommand token has been observed but the macro name has
                # yet to be read from the file. Attempt a search using the
                # newly read line.
                match = re.search('([A-Za-z]+)', line)
                if match:
                    # Macro name found
                    name  = match.group(1)
                    state = State.DOBJ_DONE

            else:
                # Begin ugly and suboptimal regex cascading due to Python...
                # Check the line for a \newcommand token
                if re.search(regex['newcommand'], line):
                    match = re.search(regex['newcommand'], line)
                    match = re.search('([A-Za-z]+)(.*)', match.group(1))
                    if match:
                        # Macro name found on the same line as \newcommand
                        name = match.group(1)
                        # Determine if the \newcommand should be interpreted as
                        # a macro or as a configurable element. We do this by
                        # checking if the current parser state is CFG_DESCR,
                        # i.e. the most recent @-token was @cfg.
                        if state == State.CFG_DESCR:
                            dobject_type = 'configurable_element'
                            brace_ctr    = 0
                            for c in match.group(2):
                                if c == '{':
                                    brace_ctr += 1
                                    if (brace_ctr == 1):
                                        continue

                                if not (brace_ctr > 0):
                                    # Ignore characters until the opening brace
                                    # for the macro definition is encountered.
                                    continue

                                # Above continue block guards against
                                # decrementing w/o having found the opening
                                # brace.
                                if c == '}':
                                    brace_ctr -= 1

                                if (brace_ctr == 0):
                                    # Definition complete, don't include this
                                    # character.
                                    state = State.DOBJ_DONE
                                    break;

                                # Append the character
                                cfg_def += c

                            if not (brace_ctr == 0):
                                raise ValueError('Configurable element {} not '
                                                 'on a single line.'
                                                 .format(name))

                        else:
                            # Assume full macro
                            dobject_type = 'macro'
                            state = State.DOBJ_DONE
                    else:
                        if state == State.CFG_DESCR:
                            dobject_type = 'configurable_element'
                        else:
                            dobject_type = 'macro'

                        # Name still to come
                        state = State.NAME

                # Check the line for a \newenvironment token
                elif re.search(regex['newenvironment'], line):
                    match = re.search(regex['newenvironment'], line)
                    match = re.search('([A-Za-z]+)', match.group(1))
                    if match:
                        # Environment name found on the same line as
                        # \newenvironment
                        name         = match.group(1)
                        dobject_type = 'environment'
                        state        = State.DOBJ_DONE
                    else:
                        # Environment name still to come
                        dobject_type = 'environment'
                        state = State.NAME

            if state == State.DOBJ_DONE:
                # Command sequence definition is complete. If the CS is valid,
                # i.e. at least one information token is defined, create
                # document object, populate and add to the corresponding
                # internal list.
                if not is_valid:
                    continue

                if dobject_type == 'macro':
                    dobject = Macro(name, descr)
                elif dobject_type == 'environment':
                    dobject = Environment(name, descr)
                elif dobject_type == 'configurable_element':
                    dobject = ConfigurableElement(name, descr, cfg_def)
                else:
                    # Invalid command sequence (should not happen)
                    raise ValueError('Parsing found invalid document object '
                                     'type \'{}\'.'
                                     .format(dobject_type))

                # Add options and arguments
                if dobject.has_opts:
                    for opt in opts:
                        if 'default' in opt:
                            dobject.add_option(
                                opt['name'], opt['descr'], opt['default'])
                        else:
                            dobject.add_option(opt['name'], opt['descr'])
                if dobject.has_args:
                    for arg in args:
                        dobject.add_argument(arg['name'], arg['descr'])

                # Register the macro as an object in the document
                dobjects[dobject_type].append(dobject)

                # Reset internal variables
                opts         = []
                args         = []
                descr        = ''
                cfg_def      = ''
                name         = ''
                state        = State.IDLE
                dobject_type = ''
                is_newline   = True
                is_valid     = False

    return dobjects
