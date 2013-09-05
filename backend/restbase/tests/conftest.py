from pyramid.testing import setUp, tearDown
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from transaction import abort
from webtest import TestApp as TestAppBase

from .. import configure, testing, utils


settings = {
    'auth.secret': 's3crit',
    'pyramid.includes': 'pyramid_mailer.testing',
    'testing': True,
}


@fixture
def config(request, tmpdir):
    config = setUp(settings=dict(settings, filesafe=str(tmpdir)))
    request.addfinalizer(tearDown)
    return config


@fixture(scope='session')
def connection(request):
    """ Sets up an SQLAlchemy engine and returns a connection
        to the database.  The connection string used can be overriden
        via the `PGDATABASE` environment variable. """
    from ..models import db_session, metadata
    engine = utils.create_db_engine(suffix='_test', **settings)
    try:
        connection = engine.connect()
    except OperationalError:
        # try to create the database...
        db_url = str(engine.url).replace(engine.url.database, 'template1')
        e = create_engine(db_url)
        c = e.connect()
        c.connection.connection.set_isolation_level(0)
        c.execute('create database %s' % engine.url.database)
        c.connection.connection.set_isolation_level(1)
        c.close()
        # ...and connect again
        connection = engine.connect()
    db_session.registry.clear()
    db_session.configure(bind=connection)
    metadata.bind = engine
    metadata.drop_all(connection.engine)
    metadata.create_all(connection.engine)
    return connection


@fixture
def db_session(config, connection, request):
    """ Returns a database session object and sets up a transaction
        savepoint, which will be rolled back after running a test. """
    trans = connection.begin()          # begin a non-orm transaction
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    from ..models import db_session
    return db_session()


def setup_app(config):
    # TODO: can we use the given `Configurator` directly?
    return configure({}, **config.registry.settings).make_wsgi_app()


class TestApp(TestAppBase):

    def get_json(self, url, params=None, headers=None, *args, **kw):
        if headers is None:
            headers = {}
        headers['Accept'] = 'application/json'
        return self.get(url, params, headers, *args, **kw)


@fixture
def app(config):
    return TestApp(setup_app(config))


@fixture
def browser(db_session, config, request):
    """ Returns an instance of `webtest.TestApp`.  The `user` pytest marker
        (`pytest.mark.user`) can be used to pre-authenticate the browser
        with the given login name: `@user('admin')`. """
    extra_environ = dict(HTTP_HOST='example.com')
    browser = TestApp(setup_app(config), extra_environ=extra_environ)
    if 'user' in request.keywords:
        # set auth cookie directly on the browser instance...
        name = request.keywords['user'].args[0]
        user = request.getfuncargvalue(name)    # get user from their fixture
        for cookie in testing.auth_cookies(str(user.id)):
            browser.cookiejar.set_cookie(cookie)
    return browser


@fixture
def alice(db_session):
    from ..principals import Principal
    return Principal(email=u'alice@foo.com', password=u'alice',
                     firstname=u'Alice', lastname=u'Kingsleigh',
                     db_session=db_session)
