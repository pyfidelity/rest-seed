"""
  New users can register an account by POSTing to ``/signup``:

  .. testsetup::

    >>> browser = getfixture('browser')

  .. doctest::

    >>> browser.post_json('http://example.com/-/signup', {
    ...   "email": "alice@example.com",
    ...   "password": "hurz"
    ... }).json['status']
    u'success'
"""

from cornice.service import Service
from colander import MappingSchema, SchemaNode, String, null
from colander import All, Email, Invalid
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid_mailer import get_mailer
from pyramid.threadlocal import get_current_request

from .. import _, principals, security, utils, path


def email_not_registered(node, param):
    """ Validator to make sure the given email is not already registered. """
    request = get_current_request()
    user = principals.find_user(param)
    if user is None:
        return True
    elif user is request.user:
        return True
    else:
        raise Invalid(node, _(node.title + u' already exists'))


class Schema(MappingSchema):
    """ Signup schema for new users. """
    firstname = SchemaNode(String(), missing=null)
    lastname = SchemaNode(String(), missing=null)
    email = SchemaNode(String(), title=u'Email',
        validator=All(Email(), email_not_registered))
    password = SchemaNode(String())


service = Service(name='signup', path=path('signup'))


@service.post(schema=Schema, accept='application/json')
def signup(request):
    signup_user(request, **request.validated)
    return dict(status='success')


def signup_user(request, **data):
    user = principals.Principal(active=False, **data)
    send_confirmation_mail(user, request)
    return user


def make_token(user):
    tokenizer = security.make_tokenizer(salt=service.name)
    return tokenizer(dict(id=user.id, email=user.email))


def send_confirmation_mail(user, request):
    url = request.route_url(service.name, _query=dict(token=make_token(user)))
    message = utils.render_mail(request=request, template='signup_confirmation',
        recipients=[user.email], subject=_(u'Please confirm your account'),
        data=dict(user=user, url=url))
    get_mailer(request).send(message)


@service.get(request_param='token')
def signup_confirm(request):
    factory = security.make_factory(salt=service.name)
    payload = factory(request)
    user = principals.find_user(payload['email'])
    if not user.active:
        user.active = True
        headers = remember(request, user.id)
        return HTTPFound(location='/', headers=headers)
    else:
        raise Forbidden
