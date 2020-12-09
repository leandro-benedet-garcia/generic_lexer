ifneq ("$(wildcard ./.env)","")
	include ./.env
	export
endif

ifeq ("$(PYTHON_EXECUTABLE)","")
	PYTHON_EXECUTABLE = python
endif

PIP = $(PYTHON_EXECUTABLE) -m pip

install-deps:
	poetry run tox --version || poetry install --no-root -E tox

tests: install-deps
	poetry run tox

docs: install-deps
	poetry run sphinx-build --version || poetry install --no-root -E docs
	cd docs && $(MAKE) html
