from .file import File
import os

def generate(source_root_dir, output_root_dir, output_dir,
             output_dirs_from_filenames):
    print('*** Cadmus documentation generator ***')
    print('Begin generating reStructuredText documents.')
    for (root_dir, dir_names, filenames) in os.walk(source_root_dir):
        for full_filename in filenames:
            (filename, file_type) = full_filename.split('.')
            # Skip unsupported file types
            if (file_type != 'sty') and \
               (file_type != 'tex'):
                continue

            # Replicate hierarchical structure in the output directory
            local_output_dir = root_dir.split(source_root_dir)[1]
            if os.name == 'nt':
                local_output_dir = local_output_dir.strip('\\')
            else:
                local_output_dir = local_output_dir.strip('/')

            # Optionally append a directory with the same name as the source
            # file to the local output directory.
            if output_dirs_from_filenames:
                local_output_dir = os.path.join(local_output_dir, filename)

            local_output_dir = os.path.join(output_root_dir, local_output_dir,
                                            output_dir)

            if not os.path.exists(local_output_dir):
                print('Creating directory ' + local_output_dir + '.')
                os.makedirs(local_output_dir)

            # Create file object
            f = File(os.path.join(root_dir, full_filename))
            # Generate RST reference documentation for defined macros.
            f.generate_rst('allsplit', local_output_dir)
            f.generate_rst('all', local_output_dir)

    print('Done generating reStructuredText documents.\n')
