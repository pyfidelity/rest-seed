from pyramid.exceptions import NotFound
from pyramid.response import FileResponse
from pyramid.view import view_config
from repoze.filesafe import open_file

from .. import models


def factory(request):
    context = models.get_content(int(request.matchdict['id']))
    if context is None:
        raise NotFound()
    return context.file


@view_config(route_name='download', permission='view', context=models.File)
def download(context, request):
    path = open_file(context.filesystem_path).name
    response = FileResponse(path=path, request=request,
        content_type=context.mimetype)
    response.headers['Content-Disposition'] = ('attachment; filename="%s"' %
        context.filename)
    return response


def includeme(config):
    config.add_route('download', '/-/{id}~', factory=factory)
