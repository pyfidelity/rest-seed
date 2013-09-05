from datetime import datetime
from pyramid.security import authenticated_userid
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Unicode

from . import models, security


def get_user(request):
    from .principals import Principal
    userid = authenticated_userid(request)
    if userid is not None:
        return Principal.query.get(userid)


def find_user(login):
    from .principals import Principal
    return Principal.query.filter(
        func.lower(Principal.email) == login.lower()).scalar()


class Principal(models.Base):
    """ An implementation of 'Principal', i.e. users and groups. """

    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    email = Column(Unicode(100), nullable=False, unique=True)
    password = Column(Unicode(100))
    firstname = Column(Unicode())
    lastname = Column(Unicode())
    creation_date = Column(DateTime(), nullable=False)
    last_login_date = Column(DateTime())

    def __init__(self, email, active=True, db_session=None, **data):
        self.email = email
        self.active = active
        self.update(**data)
        self.creation_date = datetime.now()
        if db_session is not None:
            db_session.add(self)
            db_session.flush()

    def __repr__(self):  # pragma: no cover
        return '<Principal %r>' % (self.fullname or self.email)

    def update(self, password=None, **data):
        if password is not None:
            self.password = security.hash_password(password)
        for key in 'email', 'firstname', 'lastname':
            if key in data:
                setattr(self, key, data[key])

    def __json__(self, request):
        return dict(id=self.id, email=self.email,
            firstname=self.firstname, lastname=self.lastname)

    @property
    def fullname(self):
        """ Build up the user's full name. """
        return ' '.join(filter(None, [self.firstname, self.lastname]))

    def validate_password(self, clear):
        """ Validate the given password and hash. """
        return security.validate_password(clear, self.password)
