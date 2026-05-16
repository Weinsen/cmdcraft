PYTHON ?= python
SPHINXBUILD = $(PYTHON) -m sphinx
SPHINXAPIDOC = $(PYTHON) -m sphinx.ext.apidoc
SOURCEDIR = .
BUILDDIR = _build

.PHONY: apidoc html

apidoc:
	$(SPHINXAPIDOC) -f -e -o _generated ../src/cmdcraft

html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"
