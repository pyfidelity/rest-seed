

def test_user(alice):
    assert alice.active
    assert alice.fullname == 'Alice Kingsleigh'
    assert alice.validate_password('alice')
    assert not alice.validate_password('alice!')
