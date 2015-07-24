from pytest import fixture, mark


@fixture
def url(testing, config):
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
    assert result['user']['roles'] == []
    assert result['user']['short_id'] == alice.short_id


@mark.user('admin')
def test_app_info_as_admin(browser, url, admin):
    result = browser.get_json(url).json
    assert result['authenticated'] is True
    assert result['user']['email'] == admin.email
    assert result['user']['roles'] == ['admin']
