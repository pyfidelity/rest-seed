from pytest import fixture
from backrest.models import Content, get_content
from backrest.models.categories import Category, Categories, CategoryGroup
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.ext.associationproxy import association_proxy


class Document(Content):

    __tablename__ = 'test_documents'

    id = Column(Integer(), ForeignKey(Content.id), primary_key=True)

    categories = association_proxy('associated_categories', attr='category',
        creator=lambda category: Categories(category=category))

    def update(self, categories=None, **data):
        if categories is not None:
            self.categories = categories
        super(Document, self).update(**data)


@fixture()
def document(db_session):
    return Document()


def test_create_category(document):
    document.update(categories=['foo'])
    updated = get_content(document.id)
    assert updated.categories == {'foo'}
    assert [c.title for c in Category.query] == ['foo']


def test_categories_are_unique(db_session):
    foo = Document(categories=['foo'])
    bar = Document(categories=['foo'])
    assert [c.title for c in Category.query] == ['foo']
    cat_ids = lambda doc: [c.category_id for c in doc.associated_categories]
    assert cat_ids(foo) == cat_ids(bar)


def test_categories_can_be_grouped(db_session):
    Category('eene', group='babbel')
    Category('meene')
    Category('muh', group='babbel')
    Category('kuh', group='tiere')
    babbel, tiere = CategoryGroup.query.order_by(CategoryGroup.title)
    assert [c.title for c in babbel.categories] == ['eene', 'muh']
    assert [c.title for c in tiere.categories] == ['kuh']
    foo = Document(categories=['eene', 'meene', 'muh'])
    bar = Document(categories=['muh', 'kuh'])
    assert {(c.category_.title, c.category_.group) for c in foo.associated_categories} == {
        ('eene', 'babbel'), ('meene', None), ('muh', 'babbel')}
    assert {(c.category_.title, c.category_.group) for c in bar.associated_categories} == {
        ('kuh', 'tiere'), ('muh', 'babbel')}
