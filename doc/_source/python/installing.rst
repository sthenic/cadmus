.. _python_installing:

**********
Installing
**********

Installing Cadmus involves cloning the source code from the `repository`_ and
using the Python package manager, `pip`_, to install the package.

.. _repository: http://gitlab.com/sthenic/cadmus
.. _pip: https://pypi.python.org/pypi/pip/

.. important::

    Cadmus is only compatible with Python 3 so make sure you use the correct
    package manager if you have multiple versions of Python installed on your
    system.

Recipe
------

1. Clone the repository (requires `Git`_)

   .. code-block:: bash

       $ git clone git@gitlab.com/sthenic/cadmus.git

2. Change your working directory to your cloned copy

   .. code-block:: bash

       $ cd cadmus

3. Install the package using pip for Python 3

   .. code-block:: bash

       $ pip install .

.. _git: https://git-scm.com/
