.PHONY: help deps clean dev install package test

help:
	@echo "  deps    - installs and configures dependencies in virtualenv"
	@echo "  clean   - removes unwanted files"
	@echo "  dev     - prepares a development environments"
	@echo "  install - install library on local system"
	@echo "  package - creates python packages for distribution"
	@echo "  test    - run tox"

deps:
	type virtualenv > /dev/null 2>&1 || pip install virtualenv
	test -d .venv || virtualenv .venv
	.venv/bin/pip install -Ur dev-requirements.txt

clean:
	rm -rf .cache/ .tox/ *.egg-info/ dist build .pytest_cache/
	find . -type f -name *.pyc -delete

dev:
	deps
	python setup.py develop

install:
	python setup.py install

package:
	python setup.py sdist bdist_wheel

test:
	type tox > /dev/null 2>&1 || pip install tox
	tox