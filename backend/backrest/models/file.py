from base64 import decodestring
from os.path import join, splitext, abspath
from re import match
from repoze.filesafe import create_file, open_file
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid1

from .. import utils
from .base import Base


class File(Base):

    id = Column(Integer(), primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    filename = Column(Unicode())
    mimetype = Column(String())
    size = Column(BigInteger())

    def __init__(self, filename, **data):
        self.uuid = uuid1()
        self.add(filename=filename, **data)

    def update(self, filename=None, data=None, uuid=None, **kw):
        super(File, self).update(**kw)
        if filename is not None:
            self.filename = filename
        if data is not None:
            base64 = match(r'^data:([\w/]+);base64,(.*)', data)
            if base64 is not None:
                self.mimetype, data = base64.groups()
                data = decodestring(data)
            self.size = len(data)
            with create_file(self.filesystem_path, 'wb') as fd:
                fd.write(data)

    @property
    def data(self):
        with open_file(self.filesystem_path, 'rb') as fd:
            data = fd.read()    # beware, this will load all data into memory!
        return data

    @property
    def path(self):
        """ Provide a filename within the storage. It will be based on a
            version 1 UUID and the given extension. """
        _, extension = splitext(self.filename)
        return '%s.%s' % (self.uuid, extension.lstrip('.'))

    @property
    def filesystem_path(self):
        """ Return the (absolute) filesystem path for the file data. """
        settings = utils.get_settings()
        return abspath(join(settings['filesafe'], self.path))

    def __json__(self, request):
        return dict(id=self.id, filename=self.filename,
            mimetype=self.mimetype, size=self.size,
            url=request.route_url('download', uuid=self.uuid))
