from colander import null
from datetime import datetime
from pytz import utc
from pyramid.security import authenticated_userid
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation, backref
from uuid import uuid4

from . import security
from .models.base import Base


def get_user(request):
    userid = authenticated_userid(request)
    if userid is not None:
        return Principal.query.get(userid)


def find_user(login):
    return Principal.query.filter(
        func.lower(Principal.email) == login.lower()).scalar()


class Principal(Base):
    """ An implementation of 'Principal', i.e. users and groups. """

    id = Column(Integer, primary_key=True)
    uuid = Column(String(12), index=True, unique=True, nullable=False)
    active = Column(Boolean)
    email = Column(Unicode(100), nullable=False, unique=True)
    password = Column(Unicode(100))
    firstname = Column(Unicode())
    lastname = Column(Unicode())
    creation_date = Column(DateTime(timezone=True), nullable=False, default=datetime.now(utc))
    last_login_date = Column(DateTime(timezone=True))
    global_roles = association_proxy('global_roles_', 'role')

    @classmethod
    def short_uuid(cls, length=12):
        while True:
            uuid = str(uuid4()).replace('-', '')[:length]
            if cls.query.filter_by(uuid=uuid).first() is None:
                return uuid

    def __init__(self, email, active=True, **data):
        self.uuid = self.short_uuid()
        self.email = email
        self.active = active
        self.add(**data)
        self.creation_date = datetime.now(utc)

    def __repr__(self):  # pragma: no cover
        return '<Principal %r>' % (self.fullname or self.email)

    def update(self, password=None, global_roles=None, **data):
        if global_roles is not None:
            self.global_roles = global_roles
        if password is not None:
            self.password = security.hash_password(password)
        for key in 'email', 'firstname', 'lastname':
            if key in data and data[key] is not null:
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


class GlobalRoles(Base):
    """ Global roles, which can be assigned to principals. """

    principal_id = Column(Integer, ForeignKey(Principal.id), primary_key=True)
    principal = relation(Principal, backref=backref('global_roles_',
        cascade='all, delete-orphan'))
    role = Column(Unicode(), primary_key=True)

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        title = self.principal.fullname or self.principal.email
        return '%s for "%s"' % (self.role, title)
