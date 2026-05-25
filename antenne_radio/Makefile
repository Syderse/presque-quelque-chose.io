PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
DATA_DIRS := data/raw data/normalized data/exports data/logs
ENV_LOADER := if [ -f ../.env.local ]; then set -a; source ../.env.local; set +a; fi; if [ -f .env.local ]; then set -a; source .env.local; set +a; fi

.PHONY: install test run export-public weekly clean-data

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

test:
	$(PYTEST)

run:
	@mkdir -p $(DATA_DIRS)
	@bash -c '$(ENV_LOADER); $(VENV)/bin/python scripts/pipeline.py'

export-public:
	$(VENV)/bin/python scripts/export/export_public.py

weekly:
	@echo ""
	@echo "=== Antenne Radio — Routine hebdomadaire $(shell date '+%Y-%m-%d') ==="
	@echo ""
	@echo "→ Récolte + pruning 18 mois..."
	@mkdir -p $(DATA_DIRS)
	@bash -c '$(ENV_LOADER); $(VENV)/bin/python scripts/pipeline.py'
	@echo ""
	@echo "→ Export public..."
	@$(VENV)/bin/python scripts/export/export_public.py
	@$(VENV)/bin/python scripts/weekly_report.py
	@echo ""
	@echo "=== Scan OK. Pour publier (geste conscient, manuel) ==="
	@echo "  git add static/antenne-radio/index.json"
	@echo "  git commit -m \"veille antenne-radio $$(date '+%Y-%m-%d')\""
	@echo "  git push"
	@echo ""

clean-data:
	rm -rf data/raw/* data/normalized/* data/exports/* data/logs/*
