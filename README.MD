# cookiecutter-fastapi

This is a fastapi cookiecutter template, which has the following features:
- [x] uses docker-compose for development (postgres, redis)
- [x] uses makefile for running commands
- [x] has a sample Dockerfile prepared
- [x] uses poetry
- [x] has a linting support
- [x] supports alembic migrations
- [x] includes authentication through the fastapi-users
- [x] includes admin through sqladmin package

### Setup

1. have python 3.11 ready
2. install the cookiecutter package `pip install cookiecutter`
3. have poetry package manager ready `pip install poetry`
4. generate your <project> `cookiecutter gh:dionysio/cookiecutter-fastapi`
5. move to your project and install dependencies:
```
cd <project>
poetry install
```
6. and you can finally run your project `make run`
7. open http://127.0.0.1:8000
