import argparse

VERSION_ = '0.1.0'

parser = argparse.ArgumentParser(
    description = 'Cadmus v' + VERSION_ + '\n\n'
    'cadmus.doc - Generate reStrucuturedText output from decorated LaTeX\n'
    '             source files.\n'
    'cadmus.fig - Generate figures from code snippets in combination with\n'
    '             template files.\n',
    formatter_class = argparse.RawTextHelpFormatter
)

parser.add_argument('-v', '--version',
                    help='Print version and exit.',
                    action='store_true')

# Parse input arguments
args = parser.parse_args()

if args.version:
    print(VERSION_)
