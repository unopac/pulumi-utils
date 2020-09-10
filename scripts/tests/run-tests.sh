#!/bin/bash
set -ex

ls

pwd

python -m pytest --cov=$PYTHON_PACKAGE_NAME --cov-fail-under=80