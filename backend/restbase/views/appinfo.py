from cornice.service import Service
from pyramid.settings import asbool

from restbase import path


app_info = Service(name='appinfo', path=path(''), renderer='json')


@app_info.get(accept='application/json')
def get_app_info(request):
    result = dict(debug=asbool(request.registry.settings.debug),
        demo=asbool(request.registry.settings.demo))
    if request.user is None:
        result['authenticated'] = False
    else:
        result['authenticated'] = True
        result['user'] = request.user.__json__(request)
    return result
