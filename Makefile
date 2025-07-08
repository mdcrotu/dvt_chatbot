.PHONY: run cli venv install clean embed search scrape

venv:
	python3 -m venv venv

install: venv
	venv/bin/pip install -r requirements.txt

run: install
	venv/bin/python app.py

cli: install
	venv/bin/python app.py cli

scrape: install
	venv/bin/python scrape_dvt_guide.py --max 200

embed: install
	venv/bin/python embed_dvt_guide.py

search: install
	venv/bin/python search_cli.py

validate_embeddings: install
	venv/bin/python test_validate_embeddings.py

test: install
	venv/bin/pytest tests/

clean:
	rm -rf __pycache__ venv *.pyc
