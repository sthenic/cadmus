import os
import json
from subprocess import Popen, DEVNULL

def generate_pdf(file, output_dir, page, passes, crop, crop_margins, verbose):
    # Check if file exists
    if not os.path.exists(file):
        raise ValueError('File \'' + file + '\' does not exist.')

    ostream = None if verbose else DEVNULL

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

def rasterize(file, output_dir, output_format, dev, verbose):
    # Check if file exists
    if not os.path.exists(file):
        raise ValueError('File \'' + file + '\' does not exist.')

    output_format = output_format.lower()

    # Validate output format
    if (output_format != 'jpg') and \
       (output_format != 'png'):
        raise ValueError('Unsupported rasterization format \'{}\'.'
                         .format(output_format))

    ostream = None if verbose else DEVNULL
    density = '200' if dev else '1500'

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

def generate_figures(source_dir, output_dir, output_format, dev, verbose):
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
                    verbose
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
                    dev,
                    verbose
                )
            except ValueError as e:
                print('ERROR: ' + str(e))
                pass
            print('')

    print('Done generating figures.\n')
    return
