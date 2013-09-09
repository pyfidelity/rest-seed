************
Installation
************


Development Requirements
========================

The application is based on the `Pyramid framework <http://docs.pylonsproject.org/en/latest/docs/pyramid.html/>`_ and requires Python 2.7, PostgreSQL and a basic development setup.


Mac OS X
--------

On Mac OS it's recommended to first install the dependencies using `brew <http://mxcl.github.com/homebrew/>`_::

    $ brew install postgres python node libpng ruby

.. note:: Even though Mac OS X ships with Python2.7 it is highly recommended to use the version provided by brew to avoid changing the system's Python setup.

To build the frontend you need to install the following npm modules. While in theory this could be done locally for this project by its Makefile, in practice it's much(!) easier to simply install them globally like so and be done with it::

    $ npm install -g yeoman generator-angular


Bootstrapping
=============

First clone the repository and change into it::

    $ cd foobar

To set up a development environment simply run::

    $ make

This assumes a PostgreSQL installation on `localhost:5432`.


Starting up
===========

For a full stack you need a running instance of the backend plus the frontend.

Backend
-------

To run the application during development use::

    $ backend/bin/pserve backend/development.ini
    Starting server in PID 76230.
    serving on http://0.0.0.0:6543

You can now visit `http://localhost:6543 <http://localhost:6543/-/>`_.


Frontend
--------

The frontend has its own development webserver which is the recommended way to access the stack during development.

For one, it performs automatic reloads in the browser when files change and secondly it proxies requests to the backend to the pyramid instance.

