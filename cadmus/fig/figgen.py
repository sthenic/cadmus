import os
import json
from re import search
from subprocess import Popen, DEVNULL
from template import Template

# Local variables (should be accepted as inputs when refactored w/ argparse)
build_dir  = '../../_build/figgen'
source_dir = '../../_source'

templates = {
    'article': './templates/article.tex',
    'spddoc': './templates/spddoc.tex'
}

class FigGenPathError(Exception):
    def __init__(self, message=''):
        super(FigGenPathError, self).__init__(message)
        return

def generate_pdf(file,
                 output_dir=None,
                 page=1,
                 passes=1,
                 crop=True,
                 crop_margins='10',
                 quiet=True):
    # Check if file exists
    if not os.path.exists(file):
        raise ValueError('File \'' + file + '\' does not exist.')

    ostream = DEVNULL if quiet else None

    # Find out some information about the input file
    (file_name, file_type) = os.path.basename(file).split('.')

    # Target input file directory if output directory is unspecified
    if not output_dir:
        output_dir = os.path.dirname(file)

    # Check file type
    if (file_type != 'tex'):
        raise ValueError('Input file type \'.tex\' expected, got \'{}\'.'
                         .format(file_type))

    # Call lualatex
    for p in range(passes):
        print('Pass {} of {}.'.format(p+1, passes))
        p_latex = Popen(
            ['lualatex', os.path.abspath(file)],
            cwd=os.path.abspath(output_dir),
            stdout=ostream,
            stderr=ostream
        )
        p_latex.wait()

    if p_latex.returncode > 0:
        return p_latex.returncode

    # Call pdfcrop if crop option is true
    if crop:
        p_pdfcrop = Popen(
            ['pdfcrop',
             '--margins', crop_margins,
             file_name + '.pdf', file_name + '.pdf'],
            cwd = os.path.abspath(output_dir),
            stdout=ostream,
            stderr=ostream
        )
        p_pdfcrop.wait()

        if p_pdfcrop.returncode > 0:
            return p_pdfcrop.returncode

    # Call ghostscript to split pages into separate documents
    p_gs = Popen(
        ['gs',
         '-sDEVICE=pdfwrite',
         '-dSAFER',
         '-o', file_name + '_%d.pdf',
         file_name + '.pdf'],
        cwd = os.path.abspath(output_dir),
        stdout=ostream,
        stderr=ostream
    )
    p_gs.wait()

    # Check if the target page exists before moving on
    source_path = os.path.join(
        os.path.abspath(output_dir),
        file_name + '_' + str(page) + '.pdf'
    )
    destination_path = os.path.join(
        os.path.abspath(output_dir),
        file_name + '.pdf'
    )

    if not os.path.exists(source_path):
        print('ERROR: Document \'{}\' did not produce the target page ({}).'
              .format(destination_path, page))
        return -1

    # Replace source PDF with the target page PDF
    os.replace(source_path, destination_path)

    return p_gs.returncode

def rasterize(file,
              output_dir = None,
              output_format = 'jpg',
              dev_mode = False,
              quiet = True):
    # Check if file exists
    if not os.path.exists(file):
        raise ValueError('File \'' + file + '\' does not exist.')

    output_format = output_format.lower()

    # Validate output format
    if (output_format != 'jpg') and \
       (output_format != 'png'):
        raise ValueError('Unsupported rasterization format \'{}\'.'
                         .format(output_format))

    ostream = DEVNULL if quiet else None
    density = '200' if dev_mode else '1500'

    # Find out some information about the input file
    input_dir = os.path.dirname(file)
    (file_name, file_type) = os.path.basename(file).split('.')

    # Target input file directory if output directory is unspecified
    if not output_dir:
        output_dir = input_dir

    # Check file type, only PDFs are supported currently although imagemagick
    # would probably be able to handle anything thrown at it.
    if (file_type != 'pdf'):
        raise ValueError('Input file type \'.pdf\' expected, got \'.{}\''
                         .format(file_type))

    p_touch = Popen(
        [
            'touch',
            os.path.abspath(
                os.path.join(output_dir, file_name + '.' + output_format)
            )
        ],
    )
    p_touch.wait()

    # Call convert (imagemagick)
    # The current working directory has to be the input file directory in order
    # to work properly. However, the output can be placed in any directory.
    convert_cmd = ''
    if os.name == 'nt':
        convert_cmd = r'C:\cygwin\bin\convert'
    else:
        convert_cmd = 'convert'

    p_convert = Popen(
        [
            convert_cmd,
            # Remove alpha layer and replace with a solid background color.
            '-background', 'white',
            '-alpha', 'remove', '-alpha', 'off',
            # Draw a thin border around the image.
            '-bordercolor', 'gray',
            '-border', '1',
            '-density', density, # Supersampling instead to preserve color space?
            '-resize', '1000x',
            '-flatten',
            file_name + '.pdf',
            os.path.abspath(
                os.path.join(output_dir, file_name + '.' + output_format)
            )
        ],
        cwd = os.path.abspath(input_dir),
        stdout=ostream,
        stderr=ostream
    )
    p_convert.wait()

    return p_convert.returncode

def get_template_path(root_dir, template):
    template_path_ret = ''
    # Check if the template is given by name
    if template not in templates:
        # Assuming it's a path, check if the file exists.
        if os.path.isabs(template):
            # Absolute path, copy straight off.
            template_path = template
        else:
            # The path is taken relative to the configuration file
            # root directory. Make the path absolute.
            template_path = os.path.abspath(os.path.join(root_dir, template))
        if not os.path.exists(template_path):
            raise FigGenPathError
        else:
            # Set to the absolute path
            template_path_ret = template_path
    else:
        # Valid template name, look up the path.
        template_path_ret = templates[template]

    return template_path_ret

def build_documents(source_dir, output_dir, default_template, default_font):
    print('Begin building documents.')

    # TODO: Test if some abspath stuff is needed after refactoring with argparse
    # Check if the template is given by name
    if default_template not in templates:
        # Assuming it's a path, check if the file exists
        if not os.path.exists(default_template):
            # Neither a valid name nor a valid path, raise an error
            raise ValueError('The default template \'{}\' is neither a valid '
                             'template name nor a valid path.'
                             .format(default_template))
    else:
        # Replace the variable with the correct path
        default_template = templates[default_template]

    if not os.path.exists(output_dir):
        print('Creating output directory ' + output_dir + '.')
        os.makedirs(output_dir)
    # else:
        # Clean up build directory (possible to safely?)

    # Perform a walk through the source directory in search of .tex files. If a
    # file is encountered, an instance of the Template class is created and
    # populated with the contents of the file. An enclosing directory is
    # created and the filled template is placed inside as a .tex file with the
    # same name as the source file.
    #
    # The source directory's hierarchical structure is replicated in the output
    # directory, i.e. the source file located at
    #   <source_dir>/<dir0>/<file0>.tex
    # will have its corresponding filled template document located at
    #   <output_dir>/<dir0>/<file0>/<file0>.tex
    # after the walk is complete.
    for (root_dir, dir_names, file_names) in os.walk(source_dir):
        if 'figgen.cfg' in file_names:
            try:
                with open(os.path.join(root_dir, 'figgen.cfg')) as cfg_file:
                    try:
                        cfg = json.load(cfg_file)
                    except ValueError: # Changed from value error in Python 3.5
                        print('WARNING: Could not parse configuration file, '
                              'skipping directory.')
                        continue
            except OSError:
                print('WARNING: Failed to open configuration file for reading, '
                      'skipping directory.')
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

        # Initialize default configuration and parse any settings present in the
        # 'figgen.cfg' file.
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
                except FigGenPathError:
                    # Neither a valid name nor a valid path.
                    print('WARNING: The default template specified in '
                          '\'{}\' is neither a valid template name nor a '
                          'valid path, skipping.'
                          .format(os.path.join(root_dir, 'figgen.cfg')))
                    continue

        # Replicate hierarchical structure in the output directory
        local_output_dir = root_dir.split(source_dir)[1]
        if os.name == 'nt':
            local_output_dir = local_output_dir.strip('\\')
        else:
            local_output_dir = local_output_dir.strip('/')
        local_output_dir = os.path.join(output_dir, local_output_dir)

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
                except FigGenPathError:
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
                    os.path.join(file_dir, 'figgen.cfg'), 'w'
                ) as cfg_file:
                    # Perform a JSON dump of the configuration object
                    json.dump({'targets': [match]}, cfg_file)
            except OSError:
                print('Failed to open configuration file for writing, '
                      'directory will be ignored during build step.')
                cfg_file.close()
                continue

    print('Done building documents.\n')
    return

def generate_figures(source_dir,
                     output_dir,
                     output_format = 'jpg',
                     dev_mode = False,
                     quiet = True):
    print('Begin generating figures.')
    if not os.path.exists(output_dir):
        print('Creating directory ' + output_dir + '.')
        os.makedirs(output_dir)

    for (root_dir, dir_names, file_names) in os.walk(source_dir):
        if 'figgen.cfg' in file_names:
            try:
                with open(os.path.join(root_dir, 'figgen.cfg')) as cfg_file:
                    try:
                        cfg = json.load(cfg_file)
                    except ValueError: # Changed from value error in Python 3.5
                        print('WARNING: Could not parse configuration file, '
                              'skipping directory.')
                        continue
            except OSError:
                print('WARNING: Failed to open configuration file for reading, '
                      'skipping directory.')
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

        # Replicate hierarchical structure in the output directory
        local_output_dir = root_dir.split(source_dir)[1]
        if os.name == 'nt':
            local_output_dir = local_output_dir.strip('\\')
        else:
            local_output_dir = local_output_dir.strip('/')
        # Strip any containment directory
        # TODO: What happens if empty?
        local_output_dir = os.path.dirname(local_output_dir)
        # Join the reduced source path to the output directory
        local_output_dir = os.path.join(output_dir, local_output_dir)
        # Create if directory if it doesn't exist
        if not os.path.exists(local_output_dir):
            print('Creating output directory ' + local_output_dir + '.')
            os.makedirs(local_output_dir)

        for full_file_name in file_names:
            # Search the targets for a matching entry using the full file name.
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
                match['page'] = 1
            if 'format' not in match:
                match['format'] = 'jpg'
            if 'passes' not in match:
                match['passes'] = 1
            if 'crop' not in match:
                match['crop'] = True
            if 'crop_margins' not in match:
                match['crop_margins'] = '10'

            # Validate settings
            if match['page'] < 1:
                print('WARNING: Invalid target page {}, '
                      'valid range: > 0. Skipping this entry.'
                      .format(match['page']))
                continue
            if match['passes'] < 1:
                print('WARNING: Invalid number of passes {} '
                      'valid range: > 0. Skipping this entry.'
                      .format(match['passes']))
                continue

            (file_name, file_type) = full_file_name.split('.')

            # Skip unsupported file types (TODO: Needed?)
            if (file_type != 'tex'):
                continue

            # Generate PDF using the same directory as the source file for the
            # output.
            print(
                'Generating PDF: \'' +
                full_file_name + '\' -> \'' +
                file_name + '.pdf\'.'
            )
            try:
                generate_pdf(
                    os.path.join(root_dir, full_file_name),
                    None,
                    match['page'],
                    match['passes'],
                    match['crop'],
                    match['crop_margins'],
                    quiet
                )
            except ValueError as e:
                print('ERROR: ' + str(e))
                pass
            print(
                'Converting to ' + match['format'].upper() + ': \'' +
                file_name + '.pdf\' -> \'' +
                file_name + '.' + match['format'] + '\'.'
            )
            # Convert to image and move to the target output direcory.
            try:
                rasterize(
                    os.path.join(root_dir, file_name + '.pdf'),
                    local_output_dir,
                    match['format'],
                    dev_mode,
                    quiet
                )
            except ValueError as e:
                print('ERROR: ' + str(e))
                pass
            print('')

    print('Done generating figures.\n')
    return

print('*** LaTeX figure generator ***')
build_documents(source_dir, build_dir, 'article', None)
generate_figures(source_dir=build_dir, output_dir=source_dir, dev_mode=True)
