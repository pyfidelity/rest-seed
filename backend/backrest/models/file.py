from base64 import decodestring
from os.path import join, splitext, abspath
from re import match
from repoze.filesafe import create_file, open_file
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from uuid import uuid1

from .. import utils
from .base import Base


class File(Base):

    id = Column(Integer(), primary_key=True, autoincrement=True)
    path = Column(String(128), nullable=False, unique=True)
    filename = Column(Unicode())
    mimetype = Column(String())
    size = Column(Integer())

    def __init__(self, filename, **data):
        self.add(filename=filename, **data)

    def update(self, filename=None, data=None, **kw):
        super(File, self).update(**kw)
        if filename is not None:
            self.filename = filename
            if self.path is None:
                _, extension = splitext(filename)
                self.path = self.generate_path(extension)
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

    @staticmethod
    def generate_path(extension):
        """ Generate a filename within the storage. It will be based on a
            version 1 UUID and the given extension. """
        return '%s.%s' % (uuid1(), extension.lstrip('.'))

    @property
    def filesystem_path(self):
        """ Return the (absolute) filesystem path for the file data. """
        settings = utils.get_settings()
        return abspath(join(settings['filesafe'], self.path))

    def __json__(self, request):
        return dict(id=self.id, filename=self.filename,
            mimetype=self.mimetype, size=self.size,
            url=request.route_url('download', id=self.id))
