### Install and serve the application
There are two ways that the API can be run and tested, conda and Docker:

#### 1. Conda
First install make sure that you [conda](https://docs.conda.io/en/latest/miniconda.html) installed
Then create a new conda environment and activate it:

```bash
conda create -n rupa python=3.10
conda activate rupa
```

Install [poetry](https://python-poetry.org/docs/) and packages

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Install the package and dependencies
```bash
make install
```

Serve the application and head to `localhost:5000/docs` to check it out
```bash
make serve
```

#### 2. Docker
Ensure that you have Docker installed

```bash 
make serve-docker
```


### Check the installation and run tests  

#### Conda
Install nox, this only needs to be done once per new environment
```bash
pip install nox
```
Run the tests
```bash
make test
```

#### Docker 
Build the latest image if necessary
```bash
make build-docker
```
Then run the tests
```bash
make test-docker
```

Alternatively docker can be run directly, this will run the same commands as the Makefile
```bash
	docker compose build
	docker compose run rupa nox 
```

https://www.geeksforgeeks.org/how-to-convert-html-to-markdown-in-python/
TODO:

Configure domain name and api keys as environment variables


1. convert the html to something?
2. Make a request to the email server
3. Add email server in configuration as environment variable that can be easily changed
4. Add tests for email server
5. Documentation on API
6. Clean up README

use ruff?
NOTE: If you’re sending from our EU infrastructure, be sure to substitute the beginning of the endpoint “https://api.mailgun.net” with “https://api.eu.mailgun.net”



I configured the application so that it will only make request to a single email server. I order to change the server the application has to be redeployed with a new configuration. I would probably prefer that the server is able to be changed by the user or based on a response code however, it depends on the applicaiton requirements. This API is configured in such a way that it would be trivial to adopt an alternative approach to email server selection. 

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

### Deployment
1. Poetry, I am using poetry as an packer manager and dependency resolver. I have found this to be the most sane option for managing python packages. 
2. CI
3. Pulumi 
