from pytest import fixture, xfail
from os.path import exists
from transaction import commit, abort


@fixture
def testfile(models, db_session):
    models.File(data='123456', filename=u'test.png')
    commit()
    return models.File.query.one()


def test_create_file(models, tmpdir, db_session):
    testfile = models.File(data='123456', filename=u'test.png')
    assert '/' not in testfile.path
    assert testfile.path.endswith('.png')
    assert testfile.filesystem_path == '%s/%s' % (tmpdir, testfile.path)
    assert testfile.filename == 'test.png'
    assert testfile.size == 6
    # the file hasn't yet been created and filled with data...
    path = testfile.filesystem_path
    assert not exists(path)
    # ...until the transaction has been finished
    commit()
    testfile = models.File.query.one()  # refetch to avoid unbound instance
    assert exists(path)
    assert open(testfile.filesystem_path).read() == '123456'


def test_create_file_with_base64_data(models, tmpdir, db_session):
    data = 'data:video/mp4;base64,MTIzNDU2'     # '123456' base64-encoded
    testfile = models.File(data=data, filename=u'test.png')
    assert testfile.filename == 'test.png'
    assert testfile.mimetype == 'video/mp4'
    assert testfile.size == 6
    commit()
    testfile = models.File.query.one()  # refetch to avoid unbound instance
    assert open(testfile.filesystem_path).read() == '123456'


def test_create_large_file(models, db_session):
    testfile = models.File(filename=u'test.txt', size=2655139905)
    assert testfile.size == 2655139905


def test_delete_file(models, testfile, db_session):
    db_session.delete(testfile)
    # the file hasn't yet been deleted...
    path = testfile.filesystem_path
    assert open(testfile.filesystem_path).read() == '123456'
    assert exists(path)
    # ...until the transaction has been finished
    commit()
    assert models.File.query.count() == 0
    xfail('the raw file still exists')  # FIXME: remove using `delete_file`
    assert not exists(path)


def test_abort_file_deletion(models, testfile, db_session):
    path = testfile.filesystem_path
    db_session.delete(testfile)
    abort()
    # the file hasn't been deleted...
    assert exists(path)
    assert open(path).read() == '123456'
    assert models.File.query.count() == 1
