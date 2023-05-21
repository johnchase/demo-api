## Install and serve the application
There are two ways that the API can be run and tested, conda and Docker:

For both Docker and Conda there are a couple environment variables that need to be set if you wish to use the functionality of the endpoint. You do not need to set these variables for testing, or if you wish to only view the API documentation.

```bash
export SENDGRID_API_KEY="your sendgrid key" 
export MAILGUN_API_KEY="your mailgun API key" 
```

If you wish to send emails with sendgrid rather than mailgun you update set an additional environment variable 

```bash
export SEND_WITH_MAILGUN=False
```

### 1. Install with Conda
First ensure sure that you have [Conda](https://docs.conda.io/en/latest/miniconda.html) installed

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

Serve the application and head to `localhost:5000/docs` to check out the documentation
```bash
make serve
```

### 2. Install with Docker
Ensure that you have [Docker](https://www.docker.com/) installed

```bash 
make serve-docker
```

## Use the API!
Once the app is served you can view the documentation at `http://localhost:5000/docs` and submit a request. 
**NOTE:** You need to have an account with MailGun or SendGrid or both, and have set the API keys as per instructions above. You will need to congiure the `from` email address based on the third party instructions

## Check the installation and run tests  

### 1. Conda
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



### NOTES:
#### framework:
I used FastAPI to build this API. The decision to use FastAPI is purely due to preference. Python is my most proficient language, and I am very familiar with FastAPI. I have used Django and Flask, and although they would be good alternatives I prefer FastAPI

This API is based on [code](https://github.com/johnchase/fastapi-factory) I wrote previously. I found I was frequently making APIs and FastAPI does not generate a default project structure in the way that something like Django does. The template repository I made was intended to be a paired down version of the [template](https://github.com/tiangolo/full-stack-fastapi-postgresql) that FastAPI provides. Although I used this template all of the work here (including the template) is my own and was generated specifically for this exercise.

### Expectations
Prior to building the API I like to set code standards. These are personal preference and by no means the only or best way to manage code quality.
1. Unit testing code coverage is 100%. There is debate as to the usefulness of 100%, and 100% code coverage doesn't guarantee good unit testing though for this project it should a reasonable expectation.
2. Code formatting. I will use Black for this project, though the specific formatter is not massively important
3. Linting. I will use Flake8 for linting. Again the specific linter it not too important, but standardization is.
4. Typing. I like to "enforce" type checking, at least to the extent possible in python 

### Testing
1. Testing should happen in a relatively automated way locally
2. Tests should check coverage, linting, typing, and formatting. I will not be including a database here so migrations will not be tested
3. I will use pytest as the testing framework, nox (a python implementation of tox) as the test environment manager, and poetry for configuration

### Deployment
1. I am using poetry as an packer manager and dependency resolver. I have found this to be the most sane option for managing python packages. 
2. The application is congiured to use either Conda or Docker. I am using docker compose as I have found it to be a nice way to manage applications as they become larger.

I configured the application so that it will only make request to a single email server. In order to change the server the application has to be redeployed with a new configuration. I would probably prefer that the server is able to be changed by the user or based on a response code, however, it depends on the application requirements. This API is configured in such a way that it would be trivial to adopt an alternative approach to email server selection. 

### Trade-offs
I would have liked to spend a bit of time on CI/CD, I was hoping to write a deployment for AWS with Pulumi but did not have time. It would have been nice to configure github to enforce the test suite, and deploy the application.

### Time Spent
I spent about 6 hours on this project. Having made an API template in the past helped to save time as much of the configuration was done. I ran into issues creating an account with SendGrid, for reasons that are not entirely clear to me I was denied creating an account, I appealed the decision but was still denied. Eventually I was able to create an account with my current work email. This was one of the more time consuming steps.  
