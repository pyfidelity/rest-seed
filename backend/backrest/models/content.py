from datetime import datetime
from pytz import utc
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.util import classproperty

from .base import Base


def get_content(id):
    """ Return content instance with the given id (or `None`). """
    return Content.query.filter_by(id=id).first()


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
    creation_date = Column(DateTime(timezone=True), nullable=False, default=datetime.now(utc))
    modification_date = Column(DateTime(timezone=True), nullable=False, default=datetime.now(utc))

    def __init__(self, **data):
        self.add(**data)

    def update(self, touch=True, **data):
        """ Iterate over all columns and set values from data. """
        super(Content, self).update(**data)
        if touch and 'modification_date' not in data:
            self.modification_date = datetime.now(utc)

    def __json__(self, request):
        return dict(id=self.id, title=self.title,
                    description=self.description,
                    creation_date=self.creation_date,
                    modification_date=self.modification_date)

    def __eq__(self, other):
        return isinstance(other, Content) and self.id == other.id
