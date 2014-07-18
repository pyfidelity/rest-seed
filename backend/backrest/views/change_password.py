"""
  Existing users can change their password by PUTing to ``/password``:

  .. testsetup::

    >>> Principal = getfixture('principals').Principal
    >>> _ = Principal(email=u'alice@foo.com', password=u'alice',
    ...   firstname=u'Alice', lastname=u'Kingsleigh')

    >>> browser = getfixture('browser')
    >>> browser.put_json('http://example.com/-/login', {
    ...   "login": "alice@foo.com",
    ...   "password": "alice"
    ... }).json['status']
    u'success'

  .. doctest::

    >>> browser.put_json('http://example.com/-/password', {
    ...   "current": "alice",
    ...   "password": "foo!"
    ... }).json['status']
    u'success'
"""

from colander import MappingSchema, SchemaNode, String
from colander import deferred, required, Function
from cornice.service import Service

from .. import _, path
from . import user_factory


@deferred
def current_missing(node, kw):
    """ Mark the current password to be required if a new one was given """
    request = kw['request']
    if request.user.password is None:
        return True
    data = request.json_body
    if data.get('password'):
        return required
    else:
        return None


@deferred
def validate_current_password(node, kw):
    """ Validator to make sure the current password was given and matches """
    request = kw['request']
    if request.user is None or request.user.password is None:
        return
    validate = request.user.validate_password
    return Function(validate, _(u'Password does not match'))


class Schema(MappingSchema):
    current = SchemaNode(String(), title=u'Current password',
        validator=validate_current_password, missing=current_missing)
    password = SchemaNode(String(), title=u'New password')


service = Service(name='password-change', path=path('password'),
    factory=user_factory)


@service.put(schema=Schema, accept='application/json', permission='edit')
def change_password(request):
    password = request.validated['password']
    request.user.update(password=password)
    return dict(status='success')
