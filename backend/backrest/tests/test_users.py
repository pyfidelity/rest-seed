from backrest.principals import Principal


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
