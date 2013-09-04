from cornice.service import Service
from datetime import datetime
from pyramid.security import remember, forget

from .. import _, path, principals


def valid_user(request):
    login = request.json_body['login']
    password = request.json_body['password']
    user = principals.find_user(login=login)
    if user is not None and user.active and user.validate_password(password):
        user.last_login_date = datetime.now()
        request.response.headers.extend(remember(request, user.id))
        request.user = user
    else:
        request.errors.add('body', 'login', _('Login failed'))


login = Service(name='login', path=path('login'), renderer='json')
logout = Service(name='logout', path=path('logout'))


@login.get(accept='application/json')
def auth_info(request):
    if request.user is None:
        return dict(authenticated=False)
    return dict(request.user.__json__(request), authenticated=True)


@login.put(validators=valid_user, accept='application/json')
def login_user(request):
    return dict(status='success', user=request.user)


@logout.put()
def logout_user(request):
    request.response.headers.extend(forget(request))
    return dict(status='success')
