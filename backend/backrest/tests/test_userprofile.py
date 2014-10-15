from pytest import fixture, mark


@fixture(scope='module')
def url(testing):
    return testing.route_url('user-profile')


@mark.user('alice')
def test_get_user_profile(browser, url, alice):
    result = browser.get_json(url).json
    assert result['email'] == alice.email
    assert result['firstname'] == alice.firstname
    assert result['lastname'] == alice.lastname


def test_get_user_profile_anonymously(browser, url, alice):
    browser.get_json(url, status=403)


@mark.user('admin')
def test_get_user_profile_as_admin(browser, testing, alice):
    url = testing.route_url('user-profile', _query=dict(email=alice.email))
    result = browser.get_json(url).json
    assert result['email'] == alice.email
    assert result['firstname'] == alice.firstname
    assert result['lastname'] == alice.lastname


@mark.user('alice')
def test_put_user_profile(browser, url, alice):
    data = dict(firstname='Alien', lastname='Species')
    browser.put_json(url, data)
    assert alice.firstname == u'Alien'
    assert alice.lastname == u'Species'


def test_put_user_profile_anonymously(browser, url, alice):
    data = dict(firstname='Alien', lastname='Species')
    browser.put_json(url, data, status=403)


@mark.user('alice')
def test_delete_own_account(browser, url, alice):
    alice.query.count() == 1
    browser.post_json(url, dict(password='alice'))
    alice.query.count() == 0


def test_delete_account_anonymous(browser, url, alice):
    browser.post_json(url, dict(password='alice'), status=403)
    alice.query.count() == 1


@mark.user('alice')
def test_delete_own_account_without_password(browser, url, alice):
    result = browser.post_json(url, dict(), status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('password', 'password is missing')]
    alice.query.count() == 1
