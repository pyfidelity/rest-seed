Architecture
------------

The project is designed as a client/server application. The server is written in Python using the `Pyramid framework <http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/>`_ and (mostly) serves and processes JSON data.

The client is a web application written in Javascript using the `AngularJS framework <http://angularjs.org>`_.

On the server this model is implemented (and persisted) using `SQLAlchemy <http://docs.sqlalchemy.org/en/latest/index.html>`_. On the client side using AngularJS's `controller concept <http://docs.angularjs.org/guide/dev_guide.mvc.understanding_controller>`_.

The JSON representation used to communicate between server and client simply consists of nested dictionaries.

Give the general securrity restrictions of browsers, both the client application and the ReST service must be hosted on the same machine. The frontend is configured at ``/``, the entry point for the JSON API is at ``/-``.


URL authority
=============

Given that the web client only ever loads the initial seed HTML from the server and that all subsequent requests are handled as XHR, we essentially have two URL namespaces. One for the JSON API (mapping services and resources to URLs) and the other for the AngularJS application which does its own (``#`` based) routing (``$routeProvider``).

This means, that the client must only call verbatim service urls it receives from the server (i.e. never compute a resource URL from an id or another URL etc.) and in turn it is the duty of the service to provide all required URLs as fully qualified, absolute URLS to the client.

OTOH the server must never return angular application URLs, only service URLS.
