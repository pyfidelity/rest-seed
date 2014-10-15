from pytest import fixture


@fixture
def alice(principals, db_session):
    return principals.Principal(email=u'alice@foo.com', password=u'alice',
        firstname=u'Alice', lastname=u'Kingsleigh')


@fixture
def bob(principals, db_session):
    return principals.Principal(email=u'bob@foo.bar', password=u'bob',
        firstname=u'Bob')


@fixture
def admin(principals, db_session):
    return principals.Principal(email=u'admin@foo.bar', global_roles=[u'admin'])
