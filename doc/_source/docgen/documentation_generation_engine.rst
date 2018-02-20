.. _docgen_engine:

*******************************
Documentation Generation Engine
*******************************

The documentation generation engine targets a source root directory and
traverses its contents in search of files ending in ``.tex``, ``.sty`` or
``.cls``. Once a matching file is found, its contents is parsed looking for
LaTeX macros or environments marked up with :ref:`docstrings
<docstring_syntax>`.

Directory Traversal
===================


Invoking the Engine
===================

The documentation generator may be invoked from the command line with

.. code-block:: bash

    $ python -mcadmus

after :ref:`installing <python_installing>` the Python package.
