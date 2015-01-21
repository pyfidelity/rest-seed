# convenience makefile to set up the backend

all: bin/pserve initdb

tests: bin/py.test
	@bin/py.test

bin/pserve bin/py.test: bin/python bin/pip setup.py
	bin/python setup.py dev
	@touch $@

bin/python bin/pip:
	virtualenv .

upload: setup.py bin/py.test
	$(MAKE) -C ../deployment
	PATH=${PWD}/bin:${PATH} ../deployment/bin/devpi upload --no-vcs --with-docs

initdb: name = $(shell bin/python setup.py --name)
initdb: bin/python
	@psql -c "" $(name) 2> /dev/null || createdb $(name) -E utf8 -T template0

clean:
	git clean -fXd

.PHONY: initdb clean tests upload
