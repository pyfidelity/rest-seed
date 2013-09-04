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


def setup_signer(salt):
    """ Instantiate a tokenizer for the given salt along with
        a matching route factory. """
    signer = URLSafeSerializer(get_secret(), salt=salt)

    def tokenizer(payload):
        return signer.dumps(payload)

    def factory(request):
        token = request.matchdict.get('token') or request.params.get('token')
        try:
            payload = signer.loads(token)
        except BadSignature:
            raise NotFound
        else:
            return payload

    return tokenizer, factory
