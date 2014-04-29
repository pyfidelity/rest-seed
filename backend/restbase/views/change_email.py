"""
  Existing users can request to change their email address by
  PUTing to ``/-/email/``:

  .. testsetup::

    >>> from restbase.principals import Principal
    >>> _ = Principal(email=u'alice@foo.com', password=u'alice',
    ...   firstname=u'Alice', lastname=u'Kingsleigh')

    >>> browser = getfixture('browser')
    >>> browser.put_json('http://example.com/-/login', {
    ...   "login": "alice@foo.com",
    ...   "password": "alice"
    ... }).json['status']
    u'success'

  .. doctest::

    >>> browser.put_json('http://example.com/-/email/', {
    ...   "email": "alice@bar.com",
    ...   "password": "alice"
    ... }).json['status']
    u'success'
"""

from colander import MappingSchema, SchemaNode, String
from colander import All, Email
from cornice.service import Service
from pyramid.httpexceptions import HTTPForbidden
from pyramid_mailer import get_mailer

from .. import _, security, utils, path
from . import signup, change_password


class Schema(MappingSchema):
    email = SchemaNode(String(), title=u'Email',
        validator=All(Email(), signup.email_not_registered))
    password = SchemaNode(String(), title=u'Current password',
        validator=change_password.validate_current_password)


service = Service(name='email-change', path=path('email/{token:.*}'))


def make_token(user, email):
    tokenizer = security.make_tokenizer(salt=service.name)
    return tokenizer((user.id, email))


def send_confirmation_mail(user, email, request):
    url = request.route_url(service.name, token=make_token(user, email))
    message = utils.render_mail(request=request, template='email_change',
        recipients=[email], subject=_('Confirm your email address'),
        data=dict(user=user, url=url))
    get_mailer(request).send(message)


@service.put(schema=Schema, accept='application/json')
def request_email_change(request):
    user = request.user
    email = request.validated['email']
    if not email == user.email:
        send_confirmation_mail(user, email, request)
    return dict(status='success')


@service.get()
def change_email(request):
    factory = security.make_factory(salt=service.name)
    id, email = factory(request)    # token payload is (id, email)
    user = request.user
    if user is None or not user.id == id:
        raise HTTPForbidden
    user.update(email=email)
    return request.redirect(target='change_email.success')
