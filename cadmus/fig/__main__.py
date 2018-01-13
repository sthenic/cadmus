import argparse
from .generate import generate

parser = argparse.ArgumentParser(description='Cadmus figure generator.')

parser.add_argument('--source-dir',
                    help='Specify the source directory.',
                    default='.')

parser.add_argument('--build-dir',
                    help='Specify the output directory.',
                    required=True)

parser.add_argument('--output-dir',
                    help='Specify the output directory.',
                    default=None)

parser.add_argument('--template',
                    help='Specify the default template.',
                    default='article')

parser.add_argument('--font',
                    help='Specify the default font.',
                    default=None)

parser.add_argument('--format',
                    help='Specify the output format.',
                    default='jpg')

parser.add_argument('--dev',
                    help='Enable developer mode. This drastically reduces the '
                         'output image quality to achieve faster build times.',
                    action='store_true')

parser.add_argument('--verbose',
                    help='Print console output from building the documents.',
                    action='store_true')

parser.add_argument('--dry-run',
                    help='Perform a dry run by generating source files and '
                         'skipping the build step.',
                    action='store_true')

# Parse input arguments
args = parser.parse_args()

# If the output directory is not specified, direct the output to the source
# directory.
if not args.output_dir:
    args.output_dir = args.source_dir

generate(args.source_dir, args.build_dir, args.output_dir, args.template,
         args.font, args.format, args.dev, args.verbose, args.dry_run)
