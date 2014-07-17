|TravisStatus|

.. |TravisStatus| image:: https://travis-ci.org/pyfidelity/rest-seed.png
.. _TravisStatus: https://travis-ci.org/pyfidelity/rest-seed


========
Overview
========

This is a "seed" package & repository to be used as a starting point for projects based on Pyramid, SQLAlchemy and PostgreSQL.  It holds some common setup & code that should be useful in most (of our) projects.  The idea is to fork this repository and then extend it with project-specific code while keeping the possibility to easily merge and reuse individual features back and forth between these projects (thanks to the common git tree).

To get going, start by renaming the package.  To do so, simply search and replace all occurences of "foobar", in particular the one in `backend/setup.py`.  The module name ("backrest") should not be changed, though, to make the above-mentioned merging more convenient.


============
Installation
============

To set up a development environment run::

  $ make


=========
Changelog
=========


v1 - Unreleased
===============

 - initial release
