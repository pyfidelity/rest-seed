from pytest import fixture, mark


@fixture
def url(testing, config):
    return testing.route_url('dummy')


def test_root_factory_anonymous(browser, url):
    browser.get_json(url, status=403)


@mark.user('alice')
def test_root_factory(browser, url, alice):
    result = browser.get_json(url).json
    assert result == dict(foo='bar')
