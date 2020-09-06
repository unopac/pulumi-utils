#!/bin/bash
set -ex

ls

pwd

python -m pytest --cov=barchart_import --cov-fail-under=80