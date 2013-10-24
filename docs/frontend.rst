Frontend
========

The frontend is a self-contained HTML5 application built on top of the AngularJS framework. It lives inside ``frontend`` and all commands here assume you are in that directory.

It has been bootstrapped using the ``generator-angular`` for ``yeoman``. 


Debugging the frontend build
============================

The frontend is built using ``grunt`` which minifies JS, CSS etc and creates the site as a self-contained folder inside ``frontend/dist``. To test it, use ``grunt server:dist``.