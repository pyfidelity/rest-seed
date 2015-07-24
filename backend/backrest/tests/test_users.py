from pytest import mark, raises
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


def test_unique_short_uuid(principals, db_session):
    from uuid import UUID, uuid4
    from sqlalchemy.exc import IntegrityError
    alice = principals.Principal(
        email=u'alice@foo.com', password=u'alice', name=u'Alice Kingsleigh')
    bob = principals.Principal(
        email=u'bob@foo.bar', password=u'bob', name=u'Bob')
    uuid = uuid4()
    alice.id = uuid
    # give bob a unique id which only differs in the last field
    bob.id = UUID(fields=uuid.fields[:-1] + (uuid.fields[-1] + 1,))
    with raises(IntegrityError) as e:
        db_session.flush()
    assert 'duplicate key value violates unique constraint "ix_unique_short_uuid"' in str(e.value.orig)
