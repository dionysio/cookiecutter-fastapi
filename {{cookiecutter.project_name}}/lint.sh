#!/bin/sh -e
set -x

autoflake --verbose --remove-all-unused-imports --recursive --remove-unused-variables --in-place .
isort . --profile black
black .
