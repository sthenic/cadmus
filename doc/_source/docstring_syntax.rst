.. _docstring_syntax:

****************
Docstring Syntax
****************

A line in the document source code that begins with ``%!`` gets picked up by the
:ref:`documentation generation engine <docgen_engine>`. This token may be
followed by the decorators listed in the table below, or raw text.

.. |docstring_descr| replace:: ``@descr``
.. |docstring_opt| replace:: ``@opt``
.. |docstring_kwarg| replace:: ``@kwarg``
.. |docstring_arg| replace:: ``@arg``

+--------------------+---------------------+
| Decorator          | Description         |
+====================+=====================+
| |docstring_descr|_ | Description text    |
+--------------------+---------------------+
| |docstring_opt|_   | Option              |
+--------------------+---------------------+
| |docstring_kwarg|_ | Keyword argument    |
+--------------------+---------------------+
| |docstring_arg|_   | Argument            |
+--------------------+---------------------+



.. _docstring_descr:

Descriptions
============

.. _docstring_opt:

Options
=======

.. _docstring_kwarg:

Keyword Arguments
=================

.. _docstring_arg:

Arguments
=========

