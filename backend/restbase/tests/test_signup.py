from pytest import fixture
from pyquery import PyQuery
from .. import testing


@fixture
def data():
    return dict(firstname='Alice', lastname='Kingsleigh',
        email='alice@example.com', password='hurz')


@fixture(scope='module')
def url():
    return testing.route_url('signup')


def test_signup_success(browser, url, data):
    from .. import principals
    count = principals.Principal.query.count()
    result = browser.post_json(url, data)
    assert result.json['status'] == 'success'
    assert result.test_app.cookies == {}
    assert principals.Principal.query.count() == count + 1
    user = principals.find_user(data['email'])
    assert user.firstname == 'Alice'
    assert user.lastname == 'Kingsleigh'


def test_signup_sends_confirmation_mail(browser, url, data, mailer):
    browser.post_json(url, data)
    mail, = mailer.outbox
    assert mail.recipients == [data['email']]
    assert 'Please confirm your account' in mail.html
    assert 'Please confirm your account' in mail.body
    # the user is not active until the link has been clicked...
    from .. import principals
    assert not principals.find_user(data['email']).active
    link = PyQuery(mail.html)('a')[0]
    result = browser.get(link.attrib['href'])
    # the user is taken to the frontpage & she is active now...
    assert result.location == 'http://example.com/'
    assert principals.find_user(data['email']).active


@fixture(scope='module')
def confirm_url(alice):
    from ..views.signup import make_token
    token = make_token(alice)
    return testing.route_url('signup', _query=dict(token=token))


def test_signup_confirmation_link_works_only_once(alice, browser, confirm_url):
    alice.active = False
    browser.get(confirm_url, status=302)
    assert alice.active
    # subsequent (anonymous) access leads to login page
    browser.get(confirm_url, status=403)


def test_incorrect_signup_confirmation_link(alice, browser, confirm_url):
    url = confirm_url[:-3] + 'xxx'          # guess the signature!
    browser.get(url, status=404)


def test_expired_signup_confirmation_link():
    NotImplemented


def test_email_address_is_invalid(browser, url, data):
    data = dict(data, email='alicekingsleigh')
    result = browser.post_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('email', 'Invalid email address')]


def test_email_address_already_exists(browser, url, data, alice):
    data = dict(data, email=alice.email)
    result = browser.post_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('email', 'Email already exists')]
