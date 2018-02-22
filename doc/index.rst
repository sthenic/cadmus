***********
Cadmus Docs
***********

Cadmus is a front-end to the `Sphinx`_ documentation generator. The tool is
written in Python3 and parses custom docstrings from a LaTeX file and generates
output files using the reStructuredText markdown language. These files may then
be included into a Sphinx build.

In addition to the documentation generator, the tool has a framework to manage
automatic figure generation from snippets of LaTeX code, normally used to
showcase a particular feature in a LaTeX package.

.. note::

    The source code may be found in the project's `GitLab repository`_.

.. _GitLab repository: https://gitlab.com/sthenic/cadmus

.. _Sphinx: http://www.sphinx-doc.org/

The documentation is organized into the following sections:

.. toctree::
    :maxdepth: 1
    :caption: Documentation Generation

    _source/docgen/documentation_generation.rst
    _source/docgen/docstring_syntax.rst

.. toctree::
    :maxdepth: 1
    :caption: Figure Generation

    _source/figgen/figure_generation.rst

.. toctree::
    :maxdepth: 1
    :caption: Python Package

    _source/python/installing.rst

.. toctree::
    :maxdepth: 1
    :caption: Sphinx Integration

    _source/sphinx_integration.rst
