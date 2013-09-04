from cookielib import Cookie, parse_ns_headers
from json import loads
from pyramid.renderers import render
from pyramid.security import remember
from pyramid.testing import DummyRequest
from py.test import mark
from urllib import unquote


# py.test markers (see http://pytest.org/latest/example/markers.html)
user = mark.user
xfail = mark.xfail


def as_dict(content, **kw):
    return dict(loads(render('json', content, DummyRequest())), **kw)


def route_url(name, **kwargs):
    return unquote(DummyRequest().route_url(name, **kwargs))


def auth_cookies(login):
    environ = dict(HTTP_HOST='example.com')
    cookies = [c for _, c in remember(DummyRequest(environ=environ), login)]
    for data in parse_ns_headers(cookies):
        name, value = data.pop(0)
        rest = dict(port='80', port_specified=True, domain_specified=True,
            path_specified=True, secure=False, expires=None, discard=False,
            comment='', comment_url=None, rest=None, domain='')
        rest.update(dict(data))
        rest['domain_initial_dot'] = rest['domain'].startswith('.')
        yield Cookie(name=name, value=value, **rest)
