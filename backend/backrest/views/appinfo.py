from cornice.service import Service
from pkg_resources import get_distribution
from pyramid.settings import asbool

from .. import path, project_name


app_info = Service(name='appinfo', path=path(''),
    renderer='json', accept='application/json')


@app_info.get()
def get_app_info(request):
    settings = request.registry.settings
    result = dict(debug=asbool(settings.debug), version=get_distribution(project_name).version)
    if request.user is None:
        result['authenticated'] = False
    else:
        result['authenticated'] = True
        result['user'] = request.user
    return result
