.. _index:

*************
:mod:`foobar`
*************

:Author: pyfidelity UG
:Version: |version|

.. module:: foobar


Bootstrapping
=============

Start here to join the team and get a local development intance up and running.

.. toctree::
    :maxdepth: 2

    installation
    resources

Developing the backend
======================

Continue here, if you develop the application

.. toctree::
    :maxdepth: 3

    backend
    rest
    api


Developing the frontend
=======================

Continue here, if you develop the frontend application

.. toctree::
    :maxdepth: 2

    frontend


Reference
=========

Keep these under your pillow :)

.. toctree::
    :maxdepth: 2

    architecture


Documentation
=============

(This) documentation is maintained with `sphinx <http://sphinx-doc.org/>`_. When writing documentation, please see the sections `reStructuredText Primer <http://sphinx-doc.org/rest.html>`_ and especially `Inline markup <http://sphinx-doc.org/markup/inline.html>`_ of the sphinx documentation for hints about how to format sections etc.

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
