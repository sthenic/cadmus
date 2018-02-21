    .. _docgen:

************************
Documentation Generation
************************

The documentation generation engine targets a source root directory and
traverses its contents in search of files ending in ``.tex``, ``.sty`` or
``.cls``. Once a matching file is found, its contents are parsed looking for
LaTeX macros or environments marked up with :ref:`docstrings
<docstring_syntax>`.

Directory Traversal
===================

The *source root directory* is traversed *top-down* in search of any LaTeX
files. Files containing valid docstrings will generate reStructuredText output
in various :ref:`formats <docgen_format>`. The complete path of the output
products may be tweaked by the user (explained shortly) but is always
constructed from the *output root directory* and the *base path*. The base path
is a reflection of the path of the source file relative to the source root
directory. For example, if

.. code::

    /path/to/source_root_directory/some_dir/some_subdir/file.sty

is the system path to the source file containing the docstrings, the base path is

.. code::

    some_dir/some_subdir

This is appended to the output root directory to create

.. code::

    /path/to/output_root_directory/some_dir/some_subdir

If the option ``--output-dirs-from-filenames`` is specified, the path is
extended to

.. code::

    /path/to/output_root_directory/some_dir/some_subdir/file

Finally, the *output directory* is appended to the path, yielding

.. code::

    /path/to/output_root_directory/some_dir/some_subdir/file/path/to/output_directory

This implies that the output directory should be specified as a relative path.
If the output directory is left unspecified, the default path ``ref/`` is used.

.. important::

    It is important that the output products are kept in their own directory
    since the generator overwrites any existing files by the same name. Use
    caution to not invoke the tool in such a way that causes data loss.

Example Structure
-----------------

To attempt to motivate why the path is constructed this way, let us look at an
example of how to organize the reStructuredText documentation for an example
package called ``package``. The package directory looks like this:

.. code::

    /path/to/package
        |_ <style_file_0.sty>
        |_ <style_file_1.sty>
        |_ <class.sty>

There are two style files and one class file. These files contain a few macros
and environments that have been marked up with docstrings.

First, we specify ``--source-root-directory=/path/to/package`` to point the
engine at the source files. Second, we specify ``--output-root-
directory=/path/to/documentation``. If we leave it at that and let Cadmus work
its magic, the output directory will look something like this:

.. code::

    /path/to/documentation
        |_ package.rst (static file)
        |_ ref/
            |_ <macro_0_in_style_file_0.rst>
            |_ <macro_1_in_style_file_0.rst>
            |_ <macro_2_in_style_file_0.rst>
            |_ <style_file_0_all.rst>
            |_ <macro_0_in_style_file_0.rst>
            |_ <macro_1_in_style_file_0.rst>
            |_ <environment_0_in_style_file_0.rst>
            |_ <style_file_0_all.rst>
            |_ <macro_0_in_class_all.rst>
            |_ <macro_1_in_class_all.rst>
            |_ <class_all.rst>

There will always be the need for some static content. Here ``package.rst`` is
used to provide a general description of the package itself. Usually, this text
would go on to include the automatically generated ``.rst`` files (using the
`include directive`_) when explaining the macros or environments defined by the
package.

.. _include directive: http://docutils.sourceforge.net/docs/ref/rst/directives.html#include

If we specify ``--output-dirs-from-filenames`` we may further compartmentalize
our documentation.

.. code::

    /path/to/documentation
        |_ style_file_0/
        |   |_ <style_file_0.rst> (static file)
        |   |_ ref/
        |   |   |_ <macro_0_in_style_file_0.rst>
        |   |   |_ <macro_1_in_style_file_0.rst>
        |   |   |_ <macro_2_in_style_file_0.rst>
        |   |   |_ <style_file_0_all.rst>
        |_ style_file_0/
        |   |_ <style_file_1.rst> (static file)
        |   |_ ref/
        |   |   |_ <macro_0_in_style_file_1.rst>
        |   |   |_ <macro_1_in_style_file_1.rst>
        |   |   |_ <environment_0_in_style_file_1.rst>
        |   |   |_ <style_file_1_all.rst>
        |_ style_file_0/
            |_ <class.rst> (static file)
            |_ ref/
                |_ <macro_0_in_class_all.rst>
                |_ <macro_1_in_class_all.rst>
                |_ <class_all.rst>

.. _docgen_format:

Output Format
=============


Invoking the Engine
===================

The documentation generator may be invoked from the command line with

.. code-block:: bash

    $ python -mcadmus.doc --help

after :ref:`installing <python_installing>` the Python package. The command
above should be used to get the most up-to-date information on the command-line
options.
