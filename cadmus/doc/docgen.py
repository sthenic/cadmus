from .file import File
import os

# Local variables (should be accepted as inputs when refactored w/ argparse)
source_dir = '../../../technogram/texroot/tex/latex'
output_dir = '../../_source'
sub_dir    = 'ref'

print('*** LaTeX RST document generator ***')
print('Begin generating RST documents.')
for (root_dir, dir_names, file_names) in os.walk(source_dir):
    for full_file_name in file_names:
        (file_name, file_type) = full_file_name.split('.')
        # Skip unsupported file types
        if (file_type != 'sty') and \
           (file_type != 'tex'):
            continue

        # Replicate hierarchical structure in the output directory
        local_output_dir = root_dir.split(source_dir)[1]
        if os.name == 'nt':
            local_output_dir = local_output_dir.strip('\\')
        else:
            local_output_dir = local_output_dir.strip('/')
        local_output_dir = os.path.join(output_dir, local_output_dir, sub_dir)

        if not os.path.exists(local_output_dir):
            print('Creating directory ' + local_output_dir + '.')
            os.makedirs(local_output_dir)

        # Create file object
        f = File(os.path.join(root_dir, full_file_name))
        # Generate RST reference documentation for defined macros.
        f.generate_rst('allsplit', local_output_dir)
        f.generate_rst('all', local_output_dir)

print('Done generating RST documents.\n')
