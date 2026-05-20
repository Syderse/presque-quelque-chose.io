PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
DATA_DIRS := data/raw data/normalized data/exports data/logs

.PHONY: install test run export-public clean-data

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

test:
	$(PYTEST)

run:
	@mkdir -p $(DATA_DIRS)
	$(VENV)/bin/python scripts/pipeline.py

export-public:
	$(VENV)/bin/python scripts/export/export_public.py

clean-data:
	rm -rf data/raw/* data/normalized/* data/exports/* data/logs/*
