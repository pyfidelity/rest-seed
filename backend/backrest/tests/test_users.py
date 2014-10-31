from pytest import mark
from backrest.principals import Principal
from backrest.security import list_roles_callback


def test_user(alice):
    assert alice.active
    assert alice.fullname == 'Alice Kingsleigh'
    assert alice.validate_password('alice')
    assert not alice.validate_password('alice!')


def test_global_roles(alice):
    assert alice.global_roles == []
    alice.update(global_roles=[u'admin', u'reseller'])
    refetched = Principal.query.filter_by(id=alice.id).one()
    assert refetched.global_roles == [u'admin', u'reseller']


@mark.user('alice')
def test_global_roles_in_callback(dummy_request, alice):
    assert list_roles_callback(alice.id, dummy_request) == []
    alice.update(global_roles=[u'admin'])
    assert list_roles_callback(alice.id, dummy_request) == ['role:admin']
