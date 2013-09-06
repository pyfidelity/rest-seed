from colander import null
from datetime import datetime
from os.path import join, splitext
from pyramid.security import Allow
from pyramid.security import Authenticated
from repoze.filesafe import create_file, open_file
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import classproperty
from uuid import uuid1
from zope.sqlalchemy import ZopeTransactionExtension

from . import utils


class Root(object):
    """ Root object with default permissions. """

    __acl__ = [
        (Allow, Authenticated, ['create', 'view']),
    ]


class Base(object):

    __acl__ = [
        (Allow, Authenticated, ['view', 'edit', 'delete']),
    ]

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def columns(self):
        """ Return names of all known database columns. """
        return self.__table__.columns.keys()

    def __iter__(self):
        """ Iterate over all columns and return existing values. """
        values = vars(self)
        for attr in self.columns:
            if attr in values:
                yield attr, values[attr]

    def __json__(self, request=None):
        return dict(self)

    def update(self, **data):
        """ Iterate over all columns and set values from data. """
        for attr in self.columns:
            if attr in data and data[attr] is not null:
                setattr(self, attr, data[attr])

    def __repr__(self):     # pragma: no cover
        return '<%s %s>' % (self.__class__.__name__, self.id)

    @classmethod
    def collection_path(cls):
        return '/-/{0}s'.format(cls.__name__.lower())

    @property
    def path(self):
        return '{0}/{1}'.format(self.collection_path(), self.id)


metadata = MetaData()
db_session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base(cls=Base)
Base.metadata = metadata
Base.query = db_session.query_property()


def get_content(id):
    """ Return content instance with the given id (or `None`). """
    return Content.query.filter_by(id=id).first()


class File(Base):

    id = Column(Integer(), primary_key=True, autoincrement=True)
    path = Column(String(128), nullable=False, unique=True)
    filename = Column(Unicode())
    mimetype = Column(String())
    size = Column(Integer())

    def __init__(self, db_session=None, **data):
        self.update(**data)
        if db_session is not None:
            db_session.add(self)
            db_session.flush()

    def update(self, filename, mimetype=None, data=None, id=None):
        self.filename = filename
        self.mimetype = mimetype
        if data is not None:
            _, extension = splitext(filename)
            self.path = self.generate_path(extension)
            self.size = len(data)
            with create_file(self.filesystem_path, 'wb') as fd:
                fd.write(data)

    @property
    def data(self):
        with open_file(self.filesystem_path, 'rb') as fd:
            data = fd.read()    # beware, this will load all data into memory!
        return data

    @staticmethod
    def generate_path(extension):
        """ Generate a filename within the storage. It will be based on a
            version 1 UUID and the given extension. """
        return '%s.%s' % (uuid1(), extension.lstrip('.'))

    @property
    def filesystem_path(self):
        """ Return the (absolute) filesystem path for the file data. """
        settings = utils.get_settings()
        return join(settings['filesafe'], self.path)

    def __json__(self, request):
        return dict(id=self.id, filename=self.filename,
            mimetype=self.mimetype, size=self.size,
            url=request.route_url('download', id=self.id))


class Content(Base):
    """ Base class for all content. Includes basic features such
        as ownership, time stamps for modification and creation. """

    @classproperty
    def __mapper_args__(cls):
        return dict(
            polymorphic_on='type',
            polymorphic_identity=cls.__name__.lower(),
            with_polymorphic='*')

    id = Column(Integer(), primary_key=True)
    type = Column(String(30), nullable=False)
    owner = Column(Unicode())
    title = Column(Unicode())
    description = Column(UnicodeText())
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)
    modification_date = Column(DateTime(), nullable=False, default=datetime.now)

    def __init__(self, db_session=None, **data):
        self.update(**data)
        if db_session is not None:
            db_session.add(self)
            db_session.flush()

    def update(self, touch=True, **data):
        """ Iterate over all columns and set values from data. """
        super(Content, self).update(**data)
        if touch and 'modification_date' not in data:
            self.modification_date = datetime.now()

    def __json__(self, request):
        return dict(id=self.id, title=self.title,
                    description=self.description,
                    creation_date=self.creation_date,
                    modification_date=self.modification_date)

    def __eq__(self, other):
        return isinstance(other, Content) and self.id == other.id
