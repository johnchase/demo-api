install: 
	poetry install 

serve:
	uvicorn app.main:app --reload

test:
	nox --session test coverage 
