run-api:
	uvicorn api.main:app --reload

run-scrape:
	python -m web_scraper.main

init-venv:
	python -m venv .venv

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
