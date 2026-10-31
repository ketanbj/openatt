PYTHON ?= python3
DIST ?= dist
CORE ?= $(if $(wildcard ../../core/pyproject.toml),../../core,../open-modality-trust/core)
TRIALS ?= 20
OUT ?= output/benchmark/latest.json
TECTONIC ?= tectonic
PYTHON_FOR_CHILD = $(if $(findstring /,$(PYTHON)),$(abspath $(PYTHON)),$(PYTHON))

.PHONY: help check-python install install-benchmark demo test lint check-docs verify-evidence check benchmark report build paper
.DEFAULT_GOAL := help

help:
	@printf '%s\n' 'Run from this repository root in a Python 3.11+ environment:' '  make install             Install local core + package + developer tools (CORE=... overrides path)' '  make install-benchmark   Also install optional benchmark/plot dependencies' '  make demo                Run the local generated-input demonstration' '  make test                Run this adapter test suite' '  make lint                Check Python lint and formatting' '  make check-docs          Check local Markdown links and headings' '  make verify-evidence     Verify recorded report arithmetic and measured source hashes' '  make check               Run lint, docs, tests and recorded-evidence checks' '  make benchmark           New run to ignored OUT=output/benchmark/latest.json (TRIALS=20)' '  make report              Regenerate tracked tables/figures from recorded evidence; see docs/development.md' '  make build               Build source archive and wheel locally (DIST=dist)' '  make paper               Rebuild the research PDF (requires TECTONIC and plotting dependencies)'

check-python:
	$(PYTHON) -c 'import sys; sys.version_info >= (3, 11) or sys.exit("Python 3.11+ is required; set PYTHON=/path/to/a/supported/python")'

install: check-python
	$(PYTHON) -c 'import pathlib,sys,tomllib; p=pathlib.Path(sys.argv[1])/"pyproject.toml"; assert p.is_file(), "Set CORE to the shared core checkout"; assert tomllib.loads(p.read_text())["project"]["name"] == "open-modality-trust-core", "CORE must identify the shared core package"' "$(CORE)"
	$(PYTHON) -m pip install -e "$(CORE)" -e '.[dev]'

install-benchmark: install
	$(PYTHON) -m pip install -e '.[benchmark]'

demo:
	$(PYTHON) -m openatt demo --output output/demo

test:
	$(PYTHON) -m pytest -q tests

lint:
	$(PYTHON) -m ruff check src tests scripts examples
	$(PYTHON) -m ruff format --check src tests scripts examples

check-docs:
	$(PYTHON) scripts/check_docs.py

verify-evidence:
	$(PYTHON) scripts/verify_evidence.py

check: lint check-docs test verify-evidence

benchmark:
	$(PYTHON) scripts/benchmark.py --trials "$(TRIALS)" --output "$(OUT)"

report:
	$(PYTHON) scripts/report.py

build:
	$(PYTHON) -m build --outdir "$(DIST)"

paper:
	$(MAKE) -C paper pdf PYTHON="$(PYTHON_FOR_CHILD)" TECTONIC="$(TECTONIC)"
