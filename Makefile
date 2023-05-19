install: 
	poetry install 

serve:
	uvicorn app.main:app --reload --port 5000

serve-docker:
	docker compose up

build-docker:
	docker compose build

test:
	nox --session 

test-docker:
	docker compose run rupa nox 
