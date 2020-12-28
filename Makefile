.PHONY = install install-dependencies disable-virtualenvs test mypy fix-style check_codequality
MODE ?= local

ifeq ($(MODE) , ci)
	POETRY_ARGS := -v --no-interaction --no-ansi
endif


install-dependencies:
	poetry install ${POETRY_ARGS} --no-root

disable-virtualenv:
	poetry config virtualenvs.create false

install:
	poetry install

test: install
	python -m pytest --cov=${PYTHON_PACKAGE_NAME} --cov-fail-under=80

mypy:
	mypy ${PYTHON_PACKAGE_NAME}/**
	mypy tests/**

fix-style:
	isort .
	black .


check_codequality: install
	flake8 .
	black . --check
