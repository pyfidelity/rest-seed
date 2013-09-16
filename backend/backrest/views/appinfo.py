from cornice.service import Service
from pkg_resources import get_distribution
from pyramid.interfaces import IRouteRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.interfaces import IViewClassifier
from pyramid.interfaces import IView
from pyramid.settings import asbool
from zope.interface import Interface

from .. import path, project_name


app_info = Service(name='appinfo', path=path(''),
    renderer='json', accept='application/json')


@app_info.get()
def get_app_info(request):
    settings = request.registry.settings
    result = dict(debug=asbool(settings.debug),
        version=get_distribution(project_name).version),
        routes=route_info(request))
    if request.user is None:
        result['authenticated'] = False
    else:
        result['authenticated'] = True
        result['user'] = request.user
    return result


def route_info(request):
    qu = request.registry.queryUtility
    for route in qu(IRoutesMapper).get_routes():
        interface = qu(IRouteRequest, name=route.name)
        callable = request.registry.adapters.lookup((IViewClassifier,
            interface, Interface), IView, name='', default=None)
        print route.name, callable
        return callable
