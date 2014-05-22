from html2text import HTML2Text
from os import environ
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render
from pyramid.threadlocal import get_current_registry
from pyramid_mailer.message import Message
from sqlalchemy import engine_from_config


def get_settings():
    return get_current_registry().settings


def create_db_engine(prefix='sqlalchemy.', suffix='', project_name=None, **settings):
    key = prefix + 'url'
    url = 'postgresql:///%%s%s' % suffix
    if 'PGDATABASE' in environ:
        settings[key] = url % environ['PGDATABASE']
    elif key not in settings:
        settings[key] = url % project_name
    settings.setdefault(prefix + 'echo', bool(environ.get('SQLALCHEMY_ECHO')))
    return engine_from_config(settings, prefix=prefix)


def html2text(html):
    """ convert given html markup to text using the `html2text` library """
    converter = HTML2Text()
    converter.body_width = 0
    return converter.handle(html).strip()


def template_path(name):
    return 'restbase:templates/%s.html' % name


def render_mail(request, recipients, template, data, subject, **kw):
    body = render(template_path(template), data, request)
    return Message(recipients=recipients, subject=subject,
        html=body, body=html2text(body), **kw)


def redirect(request, target, params=(), **kw):
    key = 'redirect.%s' % target
    url = request.registry.settings[key] % params
    return HTTPFound(location=url, **kw)
