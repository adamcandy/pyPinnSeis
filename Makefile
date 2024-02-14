# Makefile for pinnseis
# Adam Candy

VERSION = $(shell python3 setup.py --version)

default: all

all:
	$(MAKE) clean
	$(MAKE) build
	$(MAKE) install
	$(MAKE) show

build:
	python3 setup.py sdist bdist_wheel

install:
	python3 -m pip -v install --upgrade dist/pinnseis-$(VERSION).tar.gz

show:
	@cd /tmp && python3 -m pip show --files pinnseis; true
	@echo "Version: $(VERSION)"

clean:
	rm -r ./output
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__ pinnseis/__pycache__

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

.PHONY: all build install show clean version versionpatch versionminor versionmajor

