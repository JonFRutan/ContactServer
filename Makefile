VENV := .venv
ACTIVATE := $(VENV)/bin/activate

install:
	source $(ACTIVATE) && pip install -r requirements.txt
