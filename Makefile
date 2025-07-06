.PHONY: run cli venv install clean

venv:
	python3 -m venv venv

install: venv
	venv/bin/pip install -r requirements.txt

run: install
	venv/bin/python app.py

cli: install
	venv/bin/python app.py cli

clean:
	rm -rf __pycache__ venv *.pyc
