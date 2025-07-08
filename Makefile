.PHONY: clean deep-clean freeze venv env-run run cli install embed search scrape

venv:
	python3 -m venv venv

env-run:
	venv/bin/python -m dotenv run -- venv/bin/python -m dvt_chatbot.app run

freeze: venv
	venv/bin/pip-compile pyproject.toml --output-file=requirements.txt
	venv/bin/pip-compile --extra dev pyproject.toml --output-file=requirements-dev.txt

dev: venv
	venv/bin/pip install -e .
	venv/bin/pip install -r requirements-dev.txt

install: venv
	venv/bin/pip install -r requirements.txt

run: install
	venv/bin/python -m dvt_chatbot.app

cli: install
	venv/bin/python -m dvt_chatbot.app cli

scrape: install
	venv/bin/python -m dvt_chatbot.scrape_dvt_guide --max 200

embed: install
	venv/bin/python -m dvt_chatbot.embed_dvt_guide

search: dev
	venv/bin/python -m dvt_chatbot.search_cli

validate_embeddings: dev
	venv/bin/python test_validate_embeddings.py

test: dev
	venv/bin/pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf dvt_chatbot.egg-info

deep-clean: clean
	rm -rf dvt_guide_data.json
	rm -rf dvt_guide_data_with_embeddings.json
	rm -rf requirements.txt requirements-dev.txt
	rm -rf venv