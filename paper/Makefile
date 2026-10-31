TECTONIC ?= tectonic
PYTHON ?= python3
OUT ?= ../output/pdf

.PHONY: pdf tables

tables:
	$(PYTHON) ../scripts/report.py

pdf: tables
	mkdir -p $(OUT)
	$(TECTONIC) --keep-logs --outdir $(OUT) main.tex
	cp $(OUT)/main.pdf openatt.pdf
