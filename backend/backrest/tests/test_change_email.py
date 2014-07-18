from pytest import fixture, mark
from pyquery import PyQuery
from urllib import unquote


@fixture(scope='module')
def url(testing):
    return testing.route_url('email-change', token='')


@mark.user('alice')
def test_change_email_validation_with_invalid_email(browser, url, alice):
    data = dict(email='hurz!', password='alice')        # the email must be valid
    result = browser.put_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('email', 'Invalid email address')]
    assert alice.email == 'alice@foo.com'


@mark.user('alice')
def test_change_email_validation_with_existing_user(browser, url, alice, bob):
    data = dict(email='bob@foo.bar', password='alice')  # the email must not exist
    result = browser.put_json(url, data, status=400).json
    assert [(e['name'], e['description']) for e in result['errors']] == [
        ('email', 'Email already exists')]
    assert alice.email == 'alice@foo.com'


@mark.user('alice')
def test_change_email_sends_validation_mail(browser, url, alice, mailer):
    data = dict(email='alice@bar.com', password='alice')
    result = browser.put_json(url, data).json
    assert result['status'] == 'success'
    # the mail address is only changed after validation...
    assert alice.email == 'alice@foo.com'
    # ...which happens via email...
    message, = mailer.outbox
    assert message.recipients == ['alice@bar.com']
    assert message.subject == 'Confirm your email address'
    assert 'Confirm email change' in message.html
    assert 'Confirm email change' in message.body
    a_tag, = PyQuery(message.html)('a')
    link = unquote(a_tag.attrib['href'])
    assert link.startswith('http://example.com/-/email/')


def test_change_email_anonymously(browser, url, alice, mailer):
    data = dict(email='alice@bar.com', password='alice')
    browser.put_json(url, data, status=403)
    assert mailer.outbox == []


@mark.user('alice')
def test_unchanged_email_does_not_send_validation_mail(browser, url, alice, mailer):
    data = dict(email=alice.email, password='alice')
    browser.put_json(url, data)
    assert mailer.outbox == []


@fixture
def confirmation_url(views, testing, alice):
    token = views.change_email.make_token(alice, 'alice@bar.com')
    return testing.route_url('email-change', token=token)


@mark.user('alice')
def test_change_email_via_validation_link(browser, confirmation_url, alice):
    # since the user will use a link (in their email), we need to GET...
    result = browser.get(confirmation_url, status=302)
    # the email address has changed and the user is redirected to the configured url
    assert alice.email == 'alice@bar.com'
    assert result.location == 'http://example.com/#/email-changed'


@mark.user('alice')
def test_change_email_with_bad_validation_link(browser, confirmation_url, alice):
    url = confirmation_url[:-3] + 'xxx'     # guess the signature!
    browser.get(url, status=404)
    # the email has not changed...
    assert alice.email == 'alice@foo.com'


def test_change_email_via_link_anonymously(browser, confirmation_url, alice):
    browser.get(confirmation_url, status=403)
    # the email has not changed...
    assert alice.email == 'alice@foo.com'


@mark.user('bob')
def test_change_email_via_link_as_other_user(browser, confirmation_url, alice, bob):
    browser.get(confirmation_url, status=403)
    # the email has not changed...
    assert alice.email == 'alice@foo.com'
