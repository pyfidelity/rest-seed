from mock import patch
from backrest import commands, principals


def test_add_user(browser, testing):
    assert principals.Principal.query.count() == 0
    with patch('backrest.commands.get_app'):
        commands.add_user(args=['alice@foo.com',
            '-p', 'foobar', '-r', 'member',
            '-f', 'Alice', '-l', 'Kingsleigh'])
    alice = principals.Principal.query.one()
    assert alice.email == 'alice@foo.com'
    assert alice.firstname == 'Alice'
    assert alice.lastname == 'Kingsleigh'
    assert alice.global_roles == ['member']
    # the user can log in right away...
    url = testing.route_url('login')
    data = dict(login=alice.email, password='foobar')
    assert browser.put_json(url, data).json['status'] == 'success'
