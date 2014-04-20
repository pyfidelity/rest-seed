from pytest import fixture
from pyquery import PyQuery
from urllib import unquote
from ..testing import route_url


@fixture
def reset_request_url(alice):
    return route_url('password-reset', token='')


def test_post_password_reset(browser, alice, reset_request_url, mailer):
    data = dict(email=u'alice@foo.com')
    result = browser.post_json(reset_request_url, data).json
    assert result['status'] == 'success'
    # but an email has been sent with the signup link...
    message, = mailer.outbox
    assert message.recipients == ['alice@foo.com']
    assert 'Reset password' in message.html
    assert 'Reset password' in message.body
    # the mail contains the invitation link
    a_tag = PyQuery(message.html)('a')[0]
    link = unquote(a_tag.attrib['href'])
    assert link.startswith('http://example.com/-/reset/')


def test_post_password_reset_for_unconfirmed_user(browser, reset_request_url, alice):
    alice.active = False
    data = dict(email=u'alice@foo.com')
    browser.post_json(reset_request_url, data, status=400)


def test_post_password_reset_validation(browser, reset_request_url):
    data = dict(email='ernie')
    result = browser.post_json(reset_request_url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('email', 'Email does not exist')]


@fixture
def reset_url(alice):
    from ..views.reset_password import make_token
    return route_url('password-reset', token=make_token(alice))


def test_get_password_reset_url(browser, reset_url):
    # since the user will use a link (in their email), we need
    # a GET handler redirecting them to the (angularjs) form...
    result = browser.get(reset_url)
    assert result.location == reset_url.replace('/-/reset', '/#/reset')


def test_get_password_reset_to_bad_url(browser, reset_url):
    url = reset_url[:-3] + 'xxx'        # guess the signature!
    browser.get(url, status=404)


def test_put_password_reset(browser, reset_url, alice):
    data = dict(password='foobar')
    result = browser.put_json(reset_url, data)
    assert result.json['status'] == 'success'
    assert alice.validate_password('foobar')


def test_put_password_reset_to_bad_url(browser, reset_url, alice):
    url = reset_url[:-3] + 'xxx'        # guess the signature!
    data = dict(password='foobar')
    browser.put_json(url, data, status=404)
    # the password has not changed...
    assert alice.validate_password('alice')


def test_password_reset_link_works_only_once():
    NotImplemented


def test_expired_password_reset_link():
    NotImplemented
