Development Conventions
-----------------------

Coding, testing and documentation conventions.

Basic conventions
=================

 * All python code must pass pyflakes and pep8 (we allow linelengths of 132, though)
 * the *master* branch must have 100% code coverage at all times.
 * all tests must pass on *master* at all times.


Testing
=======

Tests are written and run using the `the pytest framework <http://pytest.org/>`_. To run them simply use::

    $ cd backend/
    $ make tests

To run an individual test, use the `-k` parameter (see `the pytest documentation <http://pytest.org/latest/usage.html#specifying-tests-selecting-tests>`_).

To create a coverage report, run::

    $ bin/py.test --cov=backrest

This generates a report on the console, as well as a pretty report in `htmlcov/index.html` where you can browse the code and see which lines are not covered::

    $ open htmlcov/index.html


Documentation
=============

Documentation is maintained with `sphinx <http://sphinx-doc.org/>`_. When writing documentation, please see the sections `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_ and especially `Inline markup <http://sphinx-doc.org/markup/inline.html>`_ of the sphinx documentation for hints about how to format sections etc.

See `PEP 257 <http://www.python.org/dev/peps/pep-0257/>`_ for docstring conventions.

The majority of the documentation should be in the code! The ``.rst`` files should be only used for meta topics -- such as this, regarding documentation ;-) -- or deployment etc.

Doc strings should start with a short sentence describing the purpose and/or reason of the method, followed by the same for each parameter (see `sphinx autoclass documentation <http://sphinx-doc.org/ext/autodoc.html>`_ and the `sphinx Python domain <http://sphinx-doc.org/domains.html#info-field-lists>`_ on how to format those.)


Building the documentation
**************************

Before merging work you need to make sure the documentation you added doesn't break anything. Do this by generating it locally by running::

  $ make docs

Make sure that doesn't result in erros or warnings and then run::

  $ open docs/htdocs/index.html

to open it in your browser to see what it looks like.
