# convenience makefile to set up the backend

all: bin/pserve initdb

bin/pserve bin/devpi: bin/python setup.py
	bin/python setup.py dev
	@touch $@

bin/python bin/pip:
	virtualenv .
	bin/pip install --upgrade setuptools pip

upload: setup.py bin/devpi
	PATH=${PWD}/bin:${PATH} bin/devpi upload --no-vcs --with-docs

initdb: name = $(shell bin/python setup.py --name)
initdb: bin/python
	@psql -c "" $(name) 2> /dev/null || createdb $(name) -E utf8 -T template0

clean:
	git clean -fXd

.PHONY: initdb clean upload
