# Makefile for pinnseis
# Adam Candy

VERSION = $(shell python3 setup.py --version)

default: all

run:
	./pinnseis.py 	

clean:
	rm -r ./output

###################################################################################################
###################################################################################################

all:
	$(MAKE) buildclean
	$(MAKE) build
	$(MAKE) install
	$(MAKE) buildshow

build:
	python3 setup.py sdist bdist_wheel

install:
	python3 -m pip -v install --upgrade dist/pinnseis-$(VERSION).tar.gz

buildshow:
	@cd /tmp && python3 -m pip show --files pinnseis; true
	@echo "Version: $(VERSION)"

buildclean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__ pinnseis/__pycache__

###################################################################################################
###################################################################################################

versionpatch:
	bumpversion --tag --commit --current-version $(VERSION) patch setup.py pinnseis/version.py pinnseis/main.py
	git push

versionminor:
	bumpversion --tag --commit --current-version $(VERSION) minor setup.py pinnseis/version.py pinnseis/main.py
	git push

versionmajor:
	bumpversion --tag --commit --current-version $(VERSION) major setup.py pinnseis/version.py pinnseis/main.py
	git push

version:
	$(MAKE) versionminor

###################################################################################################
###################################################################################################

.PHONY: all build install show clean version versionpatch versionminor versionmajor

