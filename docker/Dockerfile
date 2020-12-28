FROM python:3.7-slim as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

ARG PYTHON_PACKAGE_NAME

ENV  POETRY_VERSION=1.0.5

RUN apt-get update && apt-get install make -y && pip install "poetry==$POETRY_VERSION"

WORKDIR /home/$PYTHON_PACKAGE_NAME

COPY poetry.lock pyproject.toml .flake8 .isort.cfg Makefile ./

RUN make disable-virtualenv MODE=ci install-dependencies

FROM builder

COPY $PYTHON_PACKAGE_NAME ./$PYTHON_PACKAGE_NAME

COPY tests ./tests

ENV PYTHON_PACKAGE_NAME ${PYTHON_PACKAGE_NAME}

RUN make mode=CI install mypy check_codequality PYTHON_PACKAGE_NAME=${PYTHON_PACKAGE_NAME} test
