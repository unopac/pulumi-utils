FROM python:3.7-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 

ARG PYTHON_PACKAGE_NAME

WORKDIR /$PYTHON_PACKAGE_NAME

ENV  POETRY_VERSION=1.0.5 

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock .
COPY pyproject.toml .
COPY $PYTHON_PACKAGE_NAME ./$PYTHON_PACKAGE_NAME


RUN poetry config virtualenvs.create false && \
    poetry install -v --no-interaction --no-ansi

COPY scripts/tests/run-tests.sh /$PYTHON_PACKAGE_NAME/run-tests.sh

COPY .flake8 .isort.cfg /$PYTHON_PACKAGE_NAME/

COPY scripts/tests/check-codequality.sh /${PYTHON_PACKAGE_NAME}/check-codequality.sh

ENV PYTHON_PACKAGE_NAME ${PYTHON_PACKAGE_NAME}

ENTRYPOINT ["./run-tests.sh"]