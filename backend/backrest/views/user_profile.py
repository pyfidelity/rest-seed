"""
  Users can change their profile data by PUTing to ``/userprofile``:

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

    >>> data = browser.get_json('http://example.com/-/userprofile').json
    >>> data['firstname']
    u'Alice'
    >>> data['lastname']
    u'Kingsleigh'

    >>> browser.put_json('http://example.com/-/userprofile', {
    ...   "firstname": "Alien",
    ...   "lastname": "Species",
    ... }).json['status']
    u'success'
"""

from cornice.service import Service
from colander import MappingSchema, SchemaNode, String, null
from pyramid.exceptions import Forbidden

from .. import path, principals
from .change_password import validate_current_password


class Schema(MappingSchema):
    """ User profile schema. """
    firstname = SchemaNode(String(), missing=null)
    lastname = SchemaNode(String(), missing=null)


service = Service(name='user-profile', path=path('userprofile'))


@service.get(accept='application/json')
def get_profile(request):
    user = request.user
    if user is None:
        raise Forbidden
    elif 'email' in request.GET and 'admin' in user.global_roles:
        email = request.GET['email']
        user = principals.Principal.query.filter_by(email=email).one()
    return user.__json__(request)


@service.put(schema=Schema, accept='application/json')
def put_profile(request):
    if request.user is None:
        raise Forbidden
    request.user.update(**request.validated)
    return dict(status='success')


class DeleteAccountSchema(MappingSchema):
    password = SchemaNode(String(), validator=validate_current_password)


@service.post(schema=DeleteAccountSchema, accept='application/json')
def delete_account(request):
    if request.user is None:
        raise Forbidden
    request.user.query.delete()
    return dict(message='goodbye')
