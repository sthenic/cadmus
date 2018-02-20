.. _docstring_syntax:

****************
Docstring Syntax
****************

A line in the document source code that begins with ``%!`` gets picked up by the
:ref:`documentation generation engine <docgen_engine>`. This token may be
followed by the decorators listed in the table below, or raw text. The same
reStrucuturedText syntax supported by Sphinx is also supported by Cadmus.

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

Following a decorator, every marked line is concatenated to form the complete
description text. The operation terminates when one of the following conditions
are met:

* another docstring decorator is encountered or
* a macro or environment is defined.

If the file ends before either one of these conditions are be met, the content
is discarded. The information gathered from the docstrings is attributed to the
next LaTeX macro or environment definition, ``\newcommand`` or
``\newenvironment``. The code block below demonstrates marking up a macro.

.. code-block:: LaTeX

    %! @descr This is the macro description. Since some macros may require
    %! longer descriptions than others, the text may of course continue on
    %! another row. As long as new rows begins with '%!', the text gets picked
    %! up by the documentation generation engine.

    %! @opt fancyoutput::false:: Activate fancy output
    %! @kwarg
    %! @arg Text to typeset
    \newcommand{\amacro}[3][]{%
        ...
    }

.. _docstring_descr:

Descriptions
============

Descriptions are initiated with the ``@descr`` decorator. The parsing preserves
leading whitespace, except for the space character expected after the ``%!``
token. Any trailing whitespace at the end of a line is trimmed. However, an
empty line is a special case, which instead inserts the newline character
``\n``.

.. important::

    Leading whitespace is preserved while trailing whitespace is trimmed before
    appending a line to the description text. A special case is an empty line,
    which instead inserts the newline character ``\n``.


The code block below provides an example of how a nested list might be created
and demonstrates inserting a newline character.

.. code-block:: LaTeX

    %! @descr
    %! One of two things is bound to happen
    %! * Outcome 1
    %!   * An acceptable result
    %! * Outcome 2
    %!   * Marginally better than outcome 1
    %!
    %! This is some text following the list.
    %!
    %! The previous line inserted a newline character, which means that this
    %! sentence starts a new section!

.. _docstring_opt:

Options
=======

An option is documented with the ``@opt`` decorator. The first word following
the decorator is taken as the option's name. Any default value enclosed in
``::`` and specified immediately after the name.

.. code-block:: LaTeX

    %! @opt someopt::default:: Text explaining the option

The rules for parsing the option's description text are identical to the rules
for the |docstring_descr|_ decorator. However, keep in mind that the information
is typeset in a table so brevity tends to give the best results. If additional
information is required, consider explaining the finer points in the general
description of the macro or environment.

.. _docstring_kwarg:

Keyword Arguments
=================

A keyword argument is documented with the ``@kwarg`` decorator. The docstring
parsing behaves exactly like the |docstring_opt|_ decorator.

.. code-block:: LaTeX

    %! @kwarg keyword Text explaining the keyword argument

.. _docstring_arg:

Arguments
=========

An argument is documented with the ``@arg`` decorator. Every line of text
following the first word are used as the argument's description. Arguments may
not have default values.

.. code-block:: LaTeX

    %! @arg name Please enter your name here



