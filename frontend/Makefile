# convenience makefile to set up the frontend

grunt = node_modules/grunt/package.json
angular = app/bower_components/angular/.bower.json

all: dist/index.html

dist/index.html: Gruntfile.js $(grunt) $(angular) $(shell git ls-files app/ )
	grunt build

$(angular): .bowerrc $(grunt)
	bower install

$(grunt): package.json
	npm install

Gruntfile.js package.json:
	$(error start by running `yo angular` (after installing yeoman using `$ npm install -g yeoman generator-angular`))

clean:
	git clean -fXd

.PHONY: clean
