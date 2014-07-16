from pytest import fixture, mark
from .. import testing


@fixture(scope='module')
def url():
    return testing.route_url('user-profile')


@mark.user('alice')
def test_get_user_profile(browser, url, alice):
    result = browser.get_json(url).json
    assert result['email'] == alice.email
    assert result['firstname'] == alice.firstname
    assert result['lastname'] == alice.lastname


def test_get_user_profile_anonymously(browser, url, alice):
    browser.get_json(url, status=403)


@mark.user('alice')
def test_put_user_profile(browser, url, alice):
    data = dict(firstname='Alien', lastname='Species')
    browser.put_json(url, data)
    assert alice.firstname == u'Alien'
    assert alice.lastname == u'Species'


def test_put_user_profile_anonymously(browser, url, alice):
    data = dict(firstname='Alien', lastname='Species')
    browser.put_json(url, data, status=403)
