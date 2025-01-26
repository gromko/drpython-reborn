# :todo: `dist` target that creates a release archive.
# :todo: Own Makefile for generating the documentation.

APP_NAME='DrPython'
APP_URL='http://drpython.sourceforge.net/'
APIDOCS_DIR='apidocs'

.PHONY: all docs apidocs clean

all:
	@echo "Use: any of the targets docs, apidocs, or clean."

docs:
	$(MAKE) -C docsrc html
	$(MAKE) documentation

documentation: docsrc/_build/html
	cp -vra docsrc/_build/html/* documentation

apidocs:
	epydoc --verbose\
		--name $(APP_NAME) \
		--url $(APP_URL) \
		--docformat "restructuredtext en" \
		--graph "classtree" \
		--show-imports \
		--include-log \
		-o $(APIDOCS_DIR) \
		.

clean:
	rm -rf *~ *.orig *.bak *.pyc $(APIDOCS_DIR)
	$(MAKE) -C docsrc clean
