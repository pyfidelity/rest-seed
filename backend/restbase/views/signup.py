from cornice.service import Service
from colander import MappingSchema, SchemaNode, String
from colander import All, Email, Invalid
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid_mailer import get_mailer
from pyramid.threadlocal import get_current_request

from .. import _, models, principals, security, utils, path


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
    name = SchemaNode(String())
    email = SchemaNode(String(), title=u'Email',
        validator=All(Email(), email_not_registered))
    password = SchemaNode(String())


service = Service(name='signup', path=path('signup'))


@service.post(schema=Schema, accept='application/json')
def signup(request):
    signup_user(request, **request.validated)
    return dict(status='success')


def signup_user(request, **data):
    user = principals.Principal(db_session=models.db_session, active=False, **data)
    send_confirmation_mail(user, request)
    return user


tokenizer, factory = security.setup_signer(salt='signup')


def make_token(user):
    return tokenizer(dict(id=user.id, email=user.email))


def send_confirmation_mail(user, request):
    url = request.route_url('signup', _query=dict(token=make_token(user)))
    message = utils.render_mail(request=request, template='signup_confirmation',
        recipients=[user.email], subject=_(u'Please confirm your account'),
        data=dict(user=user, url=url))
    get_mailer(request).send(message)


@service.get(request_param='token', factory=factory)
def signup_confirm(request):
    # FIXME: the payload should be in `request.context`, but for some reason
    #   the factory doesn't get set for this route
    payload = factory(request)
    user = principals.find_user(payload['email'])
    if not user.active:
        user.active = True
        headers = remember(request, user.id)
        return HTTPFound(location='/', headers=headers)
    else:
        raise Forbidden
