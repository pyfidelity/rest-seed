"""
    Existing users can request a password reset by POSTing to ``/reset/``:

    >>> from restbase.principals import Principal
    >>> _ = Principal(email=u'alice@foo.com', password=u'alice',
    ...   firstname=u'Alice', lastname=u'Kingsleigh')

    >>> browser = getfixture('browser')
    >>> browser.post_json('http://example.com/-/reset/', {
    ...   "email": "alice@foo.com"
    ... }).json['status']
    u'success'
"""

from colander import MappingSchema, SchemaNode, String, Invalid
from cornice.service import Service
from pyramid_mailer import get_mailer

from .. import _, principals, security, utils, path


service = Service(name='password-reset', path=path('reset/{token:.*}'))


def existing_user(node, param):
    user = principals.find_user(param)
    if user is not None and user.active:
        return True
    else:
        raise Invalid(node, _('Email does not exist'))


class Schema(MappingSchema):
    email = SchemaNode(String(), title=u'Email', validator=existing_user)


@service.post(schema=Schema, accept='application/json')
def forgot_password(request):
    user = principals.find_user(request.validated['email'])
    send_password_reset_mail(user, request)
    return dict(status='success')


def make_token(user):
    tokenizer = security.make_tokenizer(salt=service.name)
    return tokenizer(dict(id=str(user.id), email=user.email))


def send_password_reset_mail(user, request):
    url = request.route_url(service.name, token=make_token(user))
    message = utils.render_mail(request=request, template='password_reset',
        recipients=[user.email], subject=_('Password reset'),
        data=dict(user=user, url=url))
    get_mailer(request).send(message)


@service.get()
def redirect_helper(request):
    factory = security.make_factory(salt=service.name)
    factory(request)        # validate the token
    return request.redirect(target='reset_password.form')


@service.put(accept='application/json')
def reset_password(request):
    factory = security.make_factory(salt=service.name)
    query = factory(request)    # the token payload is used to find the user
    user = principals.Principal.query.filter_by(**query).one()
    user.update(password=request.json_body['password'])
    return dict(status='success')
