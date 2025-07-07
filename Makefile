.PHONY: run cli venv install clean embed

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

clean:
	rm -rf __pycache__ venv *.pyc
