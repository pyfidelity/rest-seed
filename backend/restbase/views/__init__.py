from cornice.resource import resource, view
from pyramid.exceptions import NotFound
from pyramid.response import Response
from pyramid.view import forbidden_view_config


from ..models import get_content, db_session, Root


@forbidden_view_config(accept='application/json')
def forbidden_view(request):
    return Response(body='Forbidden', status='403 Forbidden')


def id_factory(request):
    """ Returns an instance of ``models.Content`` for the given ``id`` in
        the request's matchdict. If no item with the id in question exists,
        ``NotFound`` is raised. """
    if request.matchdict is not None and 'id' in request.matchdict:
        context = get_content(int(request.matchdict['id']))
        if context is None:
            raise NotFound()
        return context
    return Root()


class Content(object):
    """ A REST resource collection for content objects.

        Every GET returns a JSON representation of the given resource, designed
        to be passed back into a PUT or POST call.

        Every POST or PUT returns a (possibly updated) representation of the
        object that has been modified back to the calling client.

        A client that wishes to perform an update should always post back the
        smallest subtree possible.

        Technically, we use pyramid's JSON renderer to generate the response,
        so in the service methods we simply return instances of our models,
        which in turn have a ``__json__`` method, which is called by the
        renderer.

        When posting or putting a resource we call its ``update`` method
        passing in the data. That method is expected to only process the keys
        that the model provides and to silently ignore any that are not. This
        behavior can be used to pass (read-only) meta data to the client, which
        by convention lives in a singly entry with a key named ``__meta__``.

        Ideally the client would never post data that contains this key, but
        even if so, it will be ignored. """

    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view(renderer='json', permission='create')
    def collection_post(self):
        return self.model(db_session=db_session, **self.request.validated)

    @view(renderer='json', permission='view')
    def collection_get(self):
        NotImplemented

    @view(renderer='json', permission='edit')
    def put(self):
        with db_session.no_autoflush:
            self.context.update(**self.request.validated)
        db_session.flush()
        db_session.expire_all()      # make sure we don't get stale data...
        return self.context

    @view(renderer='json', permission='view')
    def get(self):
        return self.context

    @view(renderer='json', permission='delete')
    def delete(self):
        db_session.delete(self.context)
        db_session.flush()


def rest_resource(model):
    collection_path = model.collection_path()
    return resource(collection_path=collection_path,
                    path='%s/{id}' % collection_path,
                    factory=id_factory, schema=model.schema)
