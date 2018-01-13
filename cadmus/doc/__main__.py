import argparse
from .generate import generate

parser = argparse.ArgumentParser(description='Cadmus documentation generator.')

parser.add_argument('--source-dir',
                    help='Specify the source directory.',
                    default='.')

parser.add_argument('--output-dir',
                    help='Specify the output directory.',
                    required=True)

parser.add_argument('--sub-dir',
                    help='Specify the subdirectory.',
                    default='ref')

args = parser.parse_args()

print(args)

generate(args.source_dir, args.output_dir, args.sub_dir)
