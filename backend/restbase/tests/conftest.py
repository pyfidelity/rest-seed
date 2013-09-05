from pytest import fixture


@fixture
def alice(db_session):
    from ..principals import Principal
    return Principal(email=u'alice@foo.com', password=u'alice',
                     firstname=u'Alice', lastname=u'Kingsleigh',
                     db_session=db_session)
