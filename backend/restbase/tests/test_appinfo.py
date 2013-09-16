from pytest import fixture, mark
from restbase import testing


@fixture
def url(config):
    return testing.route_url('appinfo')


def test_app_info_anonymous(browser, url):
    result = browser.get_json(url).json
    assert result['authenticated'] is False
    assert 'user' not in result


@mark.user('alice')
def test_app_info(browser, url, alice):
    result = browser.get_json(url).json
    assert result['authenticated'] is True
    assert result['user']['email'] == alice.email
