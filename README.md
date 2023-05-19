## API Demonstration for RUPA Health

### NOTES:
This API is based on [code](https://github.com/johnchase/fastapi-factory) that I wrote previously. I found I was frequently making APIs and FastAPI does not generate a default project structure in the way that something like Django does. The template repository I made was intended to be a paired down version of the [template](https://github.com/tiangolo/full-stack-fastapi-postgresql) that FastAPI provides. 

### Expectations
Prior to building the API I like to set code standards.
1. Unit testing code coverage is 100%. There is debate as to the usefulness of 100%, and 100% code coverage doesn't guarantee good unit testing though for this project it should a reasonable expectation.
2. Code formatting. I will use Black for this project, though the specific formatter is not massively important
3. Linting. I will use Flake8 for linting. Again the specific linter it not too important, but standardization is

### Testing
1. Testing should happen in a relatively automated way locally, and enforced on github
2. Tests should check coverage, linting, and formatting. I will not be including a database here so migrations will not be tested
3. I will use pytest as the testing framework, nox (a python implementation of tox) as the test environment manager, and poetry for configurationi




### Installation
There are two ways that the API can be run and tested:

#### 1. Conda
First install poetry 
Install poetry and packages

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
make install
```


## Development
Install development version
```
make install-dev
```
### Create a database 
```
create database fastapi_db;
create user thatsyou with password 'changethis';
ALTER ROLE thatsyou SET client_encoding TO 'utf8';
ALTER ROLE thatsyou SET default_transaction_isolation TO 'read committed';
ALTER ROLE thatsyou SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db to thatsyou;
```

### Set the environment variables
```
export POSTGRES_SERVER="localhost"
export POSTGRES_USER="thatsyou"
export POSTGRES_PASSWORD="changethis"
export POSTGRES_DB="fastapi_db"
export POSTGRES_TEST_DB="nameoftestdatabase"
```

### Create the database migration
```
make migrations
```

### Run the migrations to update the tables in the database
```
make build
```
### Check the installation  

```
make test
```

Serve the application
```
make serve
```

