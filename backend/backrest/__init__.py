# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import JSON
from pyramid.settings import asbool
from sqlalchemy.orm.query import Query
from transaction import commit

from .models import db_session, metadata, Root
from .principals import get_user
from .security import list_roles_callback
from .utils import create_db_engine, redirect


# project/package name
project_name = 'foobar'


# prepare for translation factory
_ = lambda string: string


def path(service):
    """ Return path — or route pattern — for the given REST service. """
    return '/-/{0}'.format(service.lower())


def datetime_adapter(obj, request):
    if obj is not None:
        return obj.isoformat()


def timedelta_adapter(obj, request):
    if obj is not None:
        return str(obj)


def query_adapter(query, request):
    class_ = query.column_descriptions[0]['entity']
    filter_ = getattr(class_, '__json_filter__', lambda data, request: data)
    results = []
    for row in query:
        if hasattr(row, '_asdict'):
            row = filter_(row._asdict(), request)
        results.append(row)
    return results


json_renderer = JSON()
json_renderer.add_adapter(datetime, datetime_adapter)
json_renderer.add_adapter(timedelta, timedelta_adapter)
json_renderer.add_adapter(Query, query_adapter)


def configure(global_config, **settings):
    config = Configurator(settings=settings)
    config.begin()
    config.include('pyramid_chameleon')
    config.set_authentication_policy(AuthTktAuthenticationPolicy(
        secret=settings['auth.secret'], hashalg='sha512', callback=list_roles_callback))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_request_property(get_user, name='user', reify=True)
    config.set_root_factory(lambda request: Root())
    config.add_request_method(redirect)
    config.add_renderer('json', json_renderer)
    config.add_renderer('.html', 'pyramid_chameleon.zpt.renderer_factory')
    config.include('.views.download')
    config.include('cornice')
    if asbool(settings.get('testing')):
        config.include('.testing')
    config.scan(ignore=['.testing', '.tests'])
    config.commit()
    return config


def db_setup(**settings):
    engine = create_db_engine(**settings)
    db_session.registry.clear()
    db_session.configure(bind=engine)
    metadata.bind = engine


def main(global_config, **settings):        # pragma: no cover, tests have own app setup
    config = configure(global_config, **settings)
    db_setup(**settings)
    commit()
    return config.make_wsgi_app()
