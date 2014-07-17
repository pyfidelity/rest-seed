Restful Services
----------------

The backend is entirely RESTful and exposes its resources using the `cornice <https://cornice.readthedocs.org/en/latest/>`_ library along with the `colander <http://docs.pylonsproject.org/projects/colander/en/latest/>`_ library for schemas and validation.

Schemas and validation
======================

For each resource we define a colander schema, which is then attached to the cornice resource. Any action against the resource will then automatically be validated against the schema by cornice. If it succeeds, the validated (and perhaps sanitized) values of the data are available on the request object as ``request.validated``. Consumers should always only access data from here. While the original data is still available on the request it may be in an unsafe state or contain additional values that are not part of the schema.

As an example::

    from colander import MappingSchema, SchemaNode, SequenceSchema
    from colander import Integer
    from .schemas import ContentSchema, FileSchema, MissingOrRequiredNode


    class Foo(ContentSchema):

        size = SchemaNode(Integer())

For defining schemas and validators refer to the `colander documentation <http://docs.pylonsproject.org/projects/colander/en/latest/basics.html#defining-a-colander-schema>`_.

If validation fails, cornice returns a 400 response for us along with a JSON body that contains the actual errors (there may be more than one, afterall). This behavior is documented `here <https://cornice.readthedocs.org/en/latest/validation.html>`_.


Declaring resources
===================

``rest-base`` contains the main components with which we define resources: ``rest_resource`` (a decorator), ``Content`` a base class, and ``Resource`` a generic resource implementation on top of cornice.

Let's look at the Foo model as an example::

    from .models import Content

    class Foo(Content):

Next, we define its schema::

        schema = schemas.Foo

Each content is identified by a global namespace ``id`` (which is already part of the Content schema, so we didn't have to include it above)::

        id = Column(Integer, ForeignKey(Content.id), primary_key=True)

Then we have the attributes of a foo::

        size = Column(Integer(), nullable=False, default=0)

Each content must provide a ``update`` method that receives key-value data and persists it. Note, that we do not perform any validation here! The assumption is that we receive already validated data, as it has passed the cornice validation. This means, that the update method can usually be called directly with with ``**request.validated``::

        def update(self, size=23, **data):
            [...]

Finally, each content must be able to render itself as valid JSON. To this end it must provide a ``__json__`` method that gets a request and must return a dictionary::

        def __json__(self, request):
            return dict(super(Foo, self).__json__(request),
                size=self.size)


Exposing resources
==================

Once the model and schema have been defined, the resource can be exposed to the nasty, scare interweb. This is done with the ``@rest_resource`` view decorator. Back to our foo example::


    from cornice.resource import view
    from sqlalchemy.sql.expression import desc

    from .views import rest_resource, Content, Resource
    from . import _, models, schemas


    @rest_resource(model=models.Foo)

The decorator ties it with model and also defines default paths (routes) via convention. It does so by adding the API root (by default ``/-/`` with the lower caseed name of the class and the same in plural form for the **collection** variant of the model, i.e. in this case ``/-/foo`` and ``/-/foos``. This behavior is also partiall defined in the ``Content`` resource which we subclass::

    class Foo(Content):
        model = models.Foo

In following method we expose ``/-/foos`` for ``GET`` and return a list of all foos in reverse chronological order::

        @view(renderer='json', permission='view')
        def collection_get(self):
            return self.model.query.order_by(desc(self.model.creation_date)).all()

Notice, that the view only needs to return instances of our (SQLAlchemy) models. Their ``__json__`` along with pyramid's built-in JSON support take care of everything else.
