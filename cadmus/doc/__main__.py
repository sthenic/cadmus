import argparse
from .generate import generate

parser = argparse.ArgumentParser(description='Cadmus documentation generator.')

parser.add_argument('--source-root-dir',
                    help='Specify the source root directory.',
                    default='.')

parser.add_argument('--output-root-dir',
                    help='Specify the output root directory.',
                    required=True)

parser.add_argument('--output-dirs-from-filenames',
                    help='Prepend the filename to the path specified by '
                         '--output-dir.',
                    action='store_true')

parser.add_argument('--output-dir',
                    help='Specify the output directory.',
                    default='ref')

parser.add_argument('--rst-cs-section-char',
                    help='Specify the adornment character used for control'
                         'sequence sections.',
                    default='-')

parser.add_argument('--rst-cs-subsection-char',
                    help='Specify the adornment character used for control'
                         'sequence subsections.',
                    default='^')

args = parser.parse_args()

# Construct RST configuration dict
rst_conf = {
    'cs_section_char': args.rst_cs_section_char,
    'cs_subsection_char': args.rst_cs_subsection_char,
    'cs_tab_size': 4
}

generate(args.source_root_dir, args.output_root_dir, args.output_dir,
         args.output_dirs_from_filenames, rst_conf)
