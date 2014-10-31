from bcrypt import gensalt, hashpw
from itsdangerous import URLSafeSerializer, BadSignature
from pyramid.exceptions import NotFound
from pyramid.threadlocal import get_current_registry


def hash_password(password, hashed=None):
    """ Generate a hash for the given password. """
    if hashed is None:
        hashed = gensalt()
    return unicode(hashpw(password.encode('utf-8'), hashed.encode('utf-8')))


def validate_password(clear, hashed):
    """ Validate the given password and hash. """
    return hash_password(clear, hashed) == hashed


def get_secret():
    settings = get_current_registry().settings
    return settings['auth.secret']


def make_tokenizer(salt):
    """ Instantiate a tokenizer for the given salt. """
    signer = URLSafeSerializer(get_secret(), salt=salt)
    return signer.dumps


def make_factory(salt):
    """ Instantiate a route factory for the given salt. """
    signer = URLSafeSerializer(get_secret(), salt=salt)

    def factory(request):
        token = request.matchdict.get('token') or request.params.get('token')
        try:
            payload = signer.loads(token)
        except BadSignature:
            raise NotFound
        else:
            return payload

    return factory


def list_roles_callback(username, request):
    """ Authentication policy callback that queries ``principals.GlobalRoles``
        to list global roles and also checks the current context in order
        to grant the "owner" role. """
    from .models import Content
    from .principals import Principal, GlobalRoles
    roles = []
    user_id = int(username)
    context = getattr(request, 'context', None)
    if isinstance(context, Principal) and context.id == user_id:
        roles.append('owner')
    elif isinstance(context, Content) and context.owner_id == user_id:
        roles.append('owner')
    for role in GlobalRoles.query.filter_by(principal_id=username):
        roles.append('role:%s' % role.role)
    return roles
