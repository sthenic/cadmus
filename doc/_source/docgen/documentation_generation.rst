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

An Example Structure
--------------------

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

Given a file ``file.sty`` with macros ``\macroa`` and ``\macrob``, environment
``enva`` and configurable elements ``\cfga`` and ``\cfgb``, the following output
products will be created:

+------------------+---------------------------------------------------+
| File             | Description                                       |
+==================+===================================================+
| ``macroa.rst``   | RST markup of ``\macroa``                         |
+------------------+---------------------------------------------------+
| ``macrob.rst``   | RST markup of ``\macrob``                         |
+------------------+---------------------------------------------------+
| ``env.rst``      | RST markup of environment ``env``                 |
+------------------+---------------------------------------------------+
| ``file_cfg.rst`` | RST markup of configurable elements ``\cfga`` and |
|                  | ``\cfgb``                                         |
+------------------+---------------------------------------------------+
| ``file_all.rst`` | RST markup of every macro and environment in      |
|                  | their order of appearance in ``file.sty``         |
+------------------+---------------------------------------------------+

.. _docgen_format_macro:

Macro
-----

The reStructuredText markup of a macro begins with a transition marker (a
horizontal line) and is followed by the macro name as a section title.

.. note::

    The section title adornment character may be specified with the option
    ``--rst-cs-section-char`` and applies to both macros and environments.

The macro name (without ``\``) is used as a label for the section, allowing
Sphinx cross-references as ``:ref:`amacro```. The markup also defines
``|amacro|_`` which utilizes the `replacement directive`_ to insert a formatted
reference to the macro. Unfortunately, due to how Sphinx implements cross-
references, this is only supported locally inside an ``.rst`` file.

The macro description is followed by the *Syntax* subsection which states the
macro syntax and forms a legend to help interpreting the information in the
upcoming subsections: *Options*, *Keyword Arguments* and *Arguments*. Each
subsection defines a table listing the options, keyword arguments and arguments,
respectively. If no options/keyword arguments/arguments are specified for the
macro, the corresponding subsection will not be included in the markup file.

.. note::

    The subsection title adornment character may be specified with the option
    ``--rst-cs-subsection-char`` and applies to both macros and environments.

.. _replacement directive:
    http://docutils.sourceforge.net/docs/ref/rst/directives.html#replacement-text


.. _docgen_format_env:

Environment
-----------

The reStructuredText markup of a macro begins with a transition marker (a
horizontal line). The section title is created by appending the environment name
to the word *Environment*.

The name of the environment with the suffix ``_env`` is used as a label for the
section, allowing Sphinx cross-references as ``:ref:`env_env```, to use the
example from earlier. As for macros, the markup also defines ``|env_env|_``
which inserts a formatted link to the environment section with the replacement
text '``env`` environment'.

The *Syntax* subsection is followed by the *Options*, *Keyword Arguments* and
*Arguments* subsections, provided they have contents to list.

.. _docgen_format_cfg:

Configurable Elements
---------------------

The reStructuredText markup of the configurable elements of a package consists
of one single table listing the elements, their descriptions and default values.


Invoking the Engine
===================

After :ref:`installing <python_installing>` the Python package, the
documentation generator may be invoked from the command line with

.. code-block:: bash

    $ python -mcadmus.doc --help

This command above should be used to get the most up-to-date information on the
command-line options.
