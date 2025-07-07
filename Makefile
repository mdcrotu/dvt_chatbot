.PHONY: run cli venv install clean embed search scrape

venv:
	python3 -m venv venv

install: venv
	venv/bin/pip install -r requirements.txt

run: install
	venv/bin/python app.py

cli: install
	venv/bin/python app.py cli

embed: install
	venv/bin/python embed_dvt_guide.py

scrape: install
	venv/bin/python scrape_dvt_guide.py --max 200

search: install
	venv/bin/python search_cli.py

test: install
	venv/bin/python test_validate_embeddings.py

clean:
	rm -rf __pycache__ venv *.pyc
