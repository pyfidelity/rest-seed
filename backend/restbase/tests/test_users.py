

def test_user(alice):
    assert alice.active
    assert alice.name == 'Alice Kingsleigh'
    assert alice.validate_password('alice')
    assert not alice.validate_password('alice!')
