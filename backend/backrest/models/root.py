from pyramid.security import Allow
from pyramid.security import Authenticated


class Root(object):
    """ Root object with default permissions. """

    __acl__ = [
        (Allow, Authenticated, ['create', 'view']),
    ]
