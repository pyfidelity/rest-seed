API Documentation
*****************

.. automodule:: backrest


Public API
==========

The public API is exposed as a RESTful JSON interface using `cornice <http://cornice.readthedocs.org/en/latest/index.html>`_ and consists of the following services.

.. note:: For frontend developers, this is the only API documentation you should need.


Signup
------

.. automodule:: backrest.views.signup


Login
-----

.. automodule:: backrest.views.login


Password reset
--------------

.. automodule:: backrest.views.reset_password


Password change
---------------

.. automodule:: backrest.views.change_password


Email change
------------

.. automodule:: backrest.views.change_email


User profile
------------

.. automodule:: backrest.views.user_profile


Base API Classes
================

The above JSON services are based on a few helper classes.

.. automodule:: backrest.views
   :members:


Base Models
===========

The below models try to provide a basis for content-like and file-like types.  The latter deal with binary data using `repoze.filesafe` in order to be transaction-safe.

.. automodule:: backrest.models
   :members:
