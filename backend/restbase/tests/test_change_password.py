from pytest import fixture, mark
from .. import testing


@fixture(scope='module')
def url():
    return testing.route_url('password-change')


@mark.user('alice')
def test_change_password(browser, url, alice):
    data = dict(password='foo!', current='alice')
    browser.put_json(url, data)
    assert alice.validate_password('foo!')


@mark.user('alice')
def test_change_password_with_wrong_current_password(browser, url, alice):
    data = dict(password='foo!', current='hurz?')
    result = browser.put_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('current', 'Password does not match')]
    assert alice.validate_password('alice')


@mark.user('alice')
def test_change_password_without_current_password(browser, url, alice):
    data = dict(password='foo!')
    result = browser.put_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('current', 'current is missing')]
    assert alice.validate_password('alice')


@mark.user('alice')
def test_set_password_without_existing_password(browser, url, alice):
    alice.password = None
    data = dict(password='foo!', current=None)
    browser.put_json(url, data)
    assert alice.validate_password('foo!')
