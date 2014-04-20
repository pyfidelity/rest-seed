API Documentation
*****************

.. automodule:: restbase


Public API
==========

The public API is exposed as a RESTful JSON interface using `cornice <http://cornice.readthedocs.org/en/latest/index.html>`_ and consists of the following services.

.. note:: For frontend developers, this is the only API documentation you should need.


Signup
------

.. automodule:: restbase.views.signup


Login
-----

.. automodule:: restbase.views.login


Password reset
--------------

.. automodule:: restbase.views.reset_password


Password change
---------------

.. automodule:: restbase.views.change_password


Base API Classes
================

The above JSON services are based on a few helper classes.

.. automodule:: restbase.views
   :members:


Base Models
===========

The below models try to provide a basis for content-like and file-like types.  The latter deal with binary data using `repoze.filesafe` in order to be transaction-safe.

.. automodule:: restbase.models
   :members:
