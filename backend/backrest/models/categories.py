from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

from .base import Base, db_session
from .content import Content


class LookupMixin(object):

    @classmethod
    def lookup(cls, title):
        with db_session.no_autoflush:
            obj = cls.query.filter_by(title=title).first()
            if obj is None:
                obj = cls(title=title)
                db_session.add(obj)
        return obj


class CategoryGroup(Base, LookupMixin):

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(Unicode, nullable=False)

    def __init__(self, title):
        self.add(title=title)       # flush after creation...


class Category(Base, LookupMixin):

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(Unicode, nullable=False, index=True)
    group_id = Column(Integer, ForeignKey(CategoryGroup.id), nullable=True)
    group_ = relationship(CategoryGroup, backref=backref('categories',
        cascade='all, delete-orphan'))
    group = association_proxy('group_', attr='title',
        creator=CategoryGroup.lookup)

    def __init__(self, title, group=None):
        self.title = title
        if group is not None:
            self.group = group

    @classmethod
    def set_group(cls, title, group):
        cls.query.filter_by(title=title).one().group = group


class Categories(Base):

    category_id = Column(Integer, ForeignKey(Category.id), primary_key=True)
    category_ = relationship(Category, backref=backref('content_ids',
        cascade='all, delete-orphan'))
    category = association_proxy('category_', attr='title',
        creator=Category.lookup)
    content_id = Column(Integer, ForeignKey(Content.id), primary_key=True)
    content = relationship(Content, backref=backref('associated_categories',
        cascade='all, delete-orphan', collection_class=set))

    def __init__(self, category):
        self.category = category

    def __repr__(self):     # pragma: no cover
        return '<%s#%s>' % (self.content_id, self.category_.title)


class CategoriesProvider(object):

    @declared_attr
    def categories(self):
        return association_proxy('associated_categories', attr='category',
            creator=lambda category: Categories(category=category))

    def update_categories(self, categories=None, **data):
        if categories is not None:
            self.categories = categories
