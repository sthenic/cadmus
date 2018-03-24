import os
import json

from .template import Template
from .common import CFG_FILE_NAME


class CadmusPathError(Exception):
    def __init__(self, message=''):
        super(CadmusPathError, self).__init__(message)
        return


TEMPLATES = {
    'article': 'templates/article.tex'
}


def get_template_path(root_dir, template):
    template_path_ret = ''
    # Check if the template is given by name
    if template not in TEMPLATES:
        # Assuming it's a path, check if the file exists.
        if os.path.isabs(template):
            # Absolute path, copy straight off.
            template_path = template
        else:
            # The path is taken relative to the configuration file
            # root directory. Make the path absolute.
            template_path = os.path.abspath(os.path.join(root_dir, template))
        if not os.path.exists(template_path):
            raise CadmusPathError
        else:
            # Set to the absolute path
            template_path_ret = template_path
    else:
        # Valid template name, look up the path.
        template_path_ret = TEMPLATES[template]

    return template_path_ret


def generate_source_files(source_root_dir, output_root_dir, default_template,
                          default_font):
    print('Begin generating TeX sources.')

    # Check if the template is given by name
    if default_template not in TEMPLATES:
        # Assuming it's a path, check if the file exists
        if not os.path.exists(default_template):
            # Neither a valid name nor a valid path, raise an error
            raise ValueError('The default template \'{}\' is neither a valid '
                             'template name nor a valid path.'
                             .format(default_template))
    else:
        # Replace the variable with the correct path
        default_template = TEMPLATES[default_template]

    if not os.path.exists(output_root_dir):
        print('Creating output directory ' + output_root_dir + '.')
        os.makedirs(output_root_dir)
    # else:
        # Clean up build directory (possible to safely?)

    # Perform a walk through the source directory in search of .tex files. If a
    # file is encountered, an instance of the Template class is created and
    # populated with the contents of the file. An enclosing directory is
    # created and the filled template is placed inside as a .tex file with the
    # same name as the source file.

    # The source directory's hierarchical structure is replicated in the output
    # directory, i.e. the source file located at
    #   <source_root_dir>/<dir0>/<file0>.tex
    # will have its corresponding filled template document located at
    #   <output_root_dir>/<dir0>/<file0>/<file0>.tex
    # after the walk is complete.
    for (root_dir, dir_names, file_names) in os.walk(source_root_dir):
        if CFG_FILE_NAME in file_names:
            try:
                with open(os.path.join(root_dir, CFG_FILE_NAME)) as cfg_file:
                    try:
                        cfg = json.load(cfg_file)
                    except ValueError:
                        # Changed from value error in Python 3.5
                        print('WARNING: Could not parse configuration file, '
                              'skipping directory.')
                        continue
            except OSError:
                print('WARNING: Failed to open configuration file for '
                      'reading, skipping directory.')
                continue
        else:
            # Continue walking until a directory with a configuration file is
            # encountered.
            continue

        # Validate configuration file contents
        if 'targets' not in cfg:
            print('WARNING: Configuration file did not contain the '
                  'required field \'targets\', skipping directory.')
            continue

        # Initialize default configuration and parse any settings present in
        # the configuration file.
        default = {
            'page': 1,
            'format': 'jpg',
            'passes': 1,
            'crop': True,
            'font': default_font,
            'crop_margins': '10',
            'template': default_template
        }

        # Transfer any default settings from the current configuration file.
        if 'default' in cfg:
            c = cfg['default']
            if 'page' in c:
                default['page'] = c['page']
            if 'format' in c:
                default['format'] = c['format']
            if 'passes' in c:
                default['passes'] = c['passes']
            if 'crop' in c:
                default['crop'] = c['crop']
            if 'font' in c:
                default['font'] = c['font']
            if 'crop_margins' in c:
                default['crop_margins'] = c['crop_margins']
            if 'template' in c:
                try:
                    default['template'] = get_template_path(root_dir,
                                                            c['template'])
                except CadmusPathError:
                    # Neither a valid name nor a valid path.
                    print('WARNING: The default template specified in '
                          '\'{}\' is neither a valid template name nor a '
                          'valid path, skipping.'
                          .format(os.path.join(root_dir, CFG_FILE_NAME)))
                    continue

        # Replicate hierarchical structure in the output directory
        local_output_dir = root_dir.split(source_root_dir)[1]
        if os.name == 'nt':
            local_output_dir = local_output_dir.strip('\\')
        else:
            local_output_dir = local_output_dir.strip('/')
        local_output_dir = os.path.join(output_root_dir, local_output_dir)

        if not os.path.exists(local_output_dir):
            print('Creating directory ' + local_output_dir + '.')
            os.makedirs(local_output_dir)

        for full_file_name in file_names:
            # Search the targets for a matching entry using the full file name.
            # We use a generator expression from which we return the first
            # match. If there is no match, None is returned.
            match = next(
                (t for t in cfg['targets']
                    if (
                        'file_name' in t.keys() and
                        t['file_name'] == full_file_name
                )
                ),
                None
            )

            # Skip if the file name if no matching target entry is found
            if not match:
                continue

            # Check target entry for keys which have default values
            if 'page' not in match:
                match['page'] = default['page']
            if 'format' not in match:
                match['format'] = default['format']
            if 'passes' not in match:
                match['passes'] = default['passes']
            if 'crop' not in match:
                match['crop'] = default['crop']
            if 'crop_margins' not in match:
                match['crop_margins'] = default['crop_margins']
            if 'font' not in match:
                match['font'] = default['font']
            if 'template' not in match:
                # Set default template. (Validated earlier.)
                match['template'] = default['template']
            else:
                try:
                    match['template'] = get_template_path(root_dir,
                                                          match['template'])
                except CadmusPathError:
                    # Neither a valid name nor a valid path.
                    print('WARNING: The template specified for \'{}\' '
                          'is neither a valid template name nor a valid '
                          'path, skipping.'.format(full_file_name))
                    continue

            # Validate settings
            if match['page'] < 1:
                print('WARNING: Invalid target page {}, '
                      'valid range: > 0. Skipping this entry.'
                      .format(match['page']))
                continue

            # Split into file name and file type
            (file_name, file_type) = full_file_name.split('.')

            # Skip unsupported file types (needed?)
            if (file_type != 'tex'):
                continue

            # Create template object
            t = Template(match['template'])

            # Insert globally defined font
            if match['font']:
                t.insert_content('\\usepackage[no-math]{fontspec}\n',
                                 'packagehead')
                t.insert_content('\\setmainfont[Ligatures=TeX]{'
                                 + match['font'] + '}\n', 'preamble')
                t.insert_content('\\usepackage[italic]{mathastext}\n',
                                 'preamble')

            # Open the file and splice the contents into the template document.
            with open(os.path.join(root_dir, full_file_name)) as f:
                for line in f:
                    line = line.lstrip()
                    if line.startswith('\\usepackage'):
                        t.insert_content(line, 'packagetail')
                    elif line.startswith('\\documentclass'):
                        t.insert_content(line, 'documentclass')
                    else:
                        t.insert_content(line, 'code')

            file_dir = os.path.join(local_output_dir, file_name)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            t.write_file(os.path.join(file_dir, file_name + '.tex'))

            # Dump the configuration object into the build directory
            try:
                with open(
                    os.path.join(file_dir, CFG_FILE_NAME), 'w'
                ) as cfg_file:
                    # Perform a JSON dump of the configuration object
                    json.dump({'targets': [match]}, cfg_file)
            except OSError:
                print('Failed to open configuration file for writing, '
                      'directory will be ignored during build step.')
                cfg_file.close()
                continue

    print('Done generating TeX sources.\n')
    return
