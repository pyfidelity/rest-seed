from pytest import fixture, mark


@fixture(scope='module')
def url(testing):
    return testing.route_url('login')


def test_login_success(browser, url, alice):
    data = dict(login=alice.email, password='alice')
    result = browser.put_json(url, data)
    assert result.json['status'] == 'success'
    assert result.json['user']['id'] == alice.id
    assert result.json['user']['firstname'] == alice.firstname
    assert result.json['user']['email'] == alice.email
    assert 'auth_tkt' in result.test_app.cookies


def test_login_failure(browser, url, alice):
    data = dict(login='alice', password='bob')
    result = browser.put_json(url, data, status=400)
    assert result.json['status'] == 'error'
    assert 'auth_tkt' not in result.test_app.cookies


@mark.user('alice')
def test_logout(testing, browser, alice):
    url = testing.route_url('logout')
    result = browser.put_json(url, {})
    assert result.json['status'] == 'success'
    cookie = result.headers['Set-Cookie']
    assert cookie.startswith('auth_tkt="";') or cookie.startswith('auth_tkt=;')


@mark.user('alice')
def test_auth_info(browser, url, alice):
    result = browser.get_json(url).json
    assert result['authenticated']
    assert result['firstname'] == alice.firstname
    assert result['email'] == alice.email


def test_auth_info_for_anonymous(browser, url):
    result = browser.get_json(url).json
    assert not result['authenticated']
