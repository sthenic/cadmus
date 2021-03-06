from .src_utils import generate_source_files
from .build_utils import generate_figures


def generate(source_root_dir, build_root_dir, output_root_dir,
             default_template, default_font, output_format, dev, verbose,
             dry_run):
    print('*** Cadmus figure generator ***')

    # Generate source files.
    generate_source_files(source_root_dir=source_root_dir,
                          output_root_dir=build_root_dir,
                          default_template=default_template,
                          default_font=default_font)

    # Generate figures unless dry_run is specified.
    if not dry_run:
        generate_figures(source_root_dir=build_root_dir,
                         output_root_dir=output_root_dir,
                         output_format=output_format,
                         dev=dev,
                         verbose=verbose)

    return
