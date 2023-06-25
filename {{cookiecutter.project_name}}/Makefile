SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

install: poetry install --with dev

run:
	poetry run python ./main.py

down:
	docker-compose down
