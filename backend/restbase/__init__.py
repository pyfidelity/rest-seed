# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import JSON

from .models import db_session, metadata, Root
from .principals import get_user
from .utils import create_db_engine, redirect


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


json_renderer = JSON()
json_renderer.add_adapter(datetime, datetime_adapter)
json_renderer.add_adapter(timedelta, timedelta_adapter)


def configure(global_config, **settings):
    config = Configurator(settings=settings)
    config.begin()
    config.include('pyramid_chameleon')
    config.set_authentication_policy(AuthTktAuthenticationPolicy(
        secret=settings['auth.secret'], hashalg='sha512'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_request_property(get_user, name='user', reify=True)
    config.set_root_factory(lambda request: Root())
    config.add_request_method(redirect)
    config.add_renderer('json', json_renderer)
    config.add_renderer('.html', 'pyramid_chameleon.zpt.renderer_factory')
    config.include('.views.download')
    config.include('cornice')
    ignore = []
    if settings.get('testing'):
        config.include('.testing')
        ignore = ['.testing', '.tests']
    config.scan(ignore=ignore)
    config.commit()
    return config


def db_setup(**settings):
    engine = create_db_engine(**settings)
    db_session.registry.clear()
    db_session.configure(bind=engine)
    metadata.bind = engine
    metadata.create_all(engine)
