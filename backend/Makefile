# convenience makefile to set up the backend

version = 2.7

all: bin/pserve initdb

tests: bin/py.test
	bin/py.test

bin/pserve bin/py.test: bin/python bin/pip setup.py
	bin/python setup.py dev
	@touch $@

bin/python bin/pip:
	virtualenv-$(version) .

upload: setup.py bin/py.test
	devpi upload --no-vcs

initdb: name = $(shell bin/python setup.py --name)
initdb: bin/python
	@psql -c "" $(name) 2> /dev/null || createdb $(name) -E utf8 -T template0

clean:
	git clean -fXd

.PHONY: initdb clean tests dist
