# convenience makefile to set up the backend

name = $(shell python setup.py --name)
version = 2.7

all: bin/pserve initdb

tests: bin/py.test
	bin/py.test

bin/pserve bin/py.test: bin/python bin/pip setup.py
	bin/pip install zope.sqlalchemy --no-deps -i https://pypi.python.org/simple/
	bin/python setup.py develop easy_install $(name)[development]
	git submodule update --init
	bin/pip install -e src/*

bin/python bin/pip:
	virtualenv-$(version) .

initdb:
	@psql -c "" $(name) 2> /dev/null || createdb $(name) -E utf8 -T template0

clean:
	git clean -fXd

.PHONY: initdb clean tests dist
