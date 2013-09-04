# convenience makefile to set up the project

parts = backend frontend docs deployment

all: $(parts)

$(parts):
	$(MAKE) -C $@

clean:
	git clean -fXd

.PHONY: clean $(parts)
