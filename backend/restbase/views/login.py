"""
  Existing users can log in using a PUT request at ``/login``:

  .. testsetup::

    >>> from restbase.principals import Principal
    >>> _ = Principal(email=u'alice@foo.com', password=u'alice',
    ...   firstname=u'Alice', lastname=u'Kingsleigh')
    >>> browser = getfixture('browser')

  .. doctest::

    >>> browser.put_json('http://example.com/-/login', {
    ...   "login": "alice@foo.com",
    ...   "password": "alice"
    ... }).json['status']
    u'success'

  While logged in the frontend may request authentication info via GET:

    >>> info = browser.get_json('http://example.com/-/login').json
    >>> info['authenticated']
    True
    >>> info['firstname'], info['lastname'], info['email']
    (u'Alice', u'Kingsleigh', u'alice@foo.com')

  Logging out again is handled via a PUT at ``/logout``:

    >>> browser.put_json('http://example.com/-/logout', {}).json['status']
    u'success'

"""

from cornice.service import Service
from datetime import datetime
from pyramid.security import remember, forget

from .. import _, path, principals


def valid_user(request):
    login = request.json_body['login']
    password = request.json_body['password']
    user = principals.find_user(login=login)
    if user is not None and user.active and user.validate_password(password):
        user.last_login_date = datetime.utcnow()
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
