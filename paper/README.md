# OPENATT research draft

**OpenATT: Scoped Controller Evidence Without Promoting Contact to Consent**

This is an experimental systems report, not a submitted/accepted paper. Authorship
must be finalized before submission. It follows OpenAVT's separation of context,
prior work, trust boundaries, implementation, measured evidence and future work.

- `main.tex`, `sections/`, `references.bib`: editable narrative and verified primary sources.
- `artifacts/measurements.tex`, channel tables/figure: generated from the raw benchmark JSON.
- `openatt.pdf`: compiled and visually inspected review copy.
- `usenix.sty`: unchanged style copied from OpenAVT's official USENIX Security 2027 template artifact. Its use does not imply venue readiness.

```sh
python openatt/scripts/report.py
cd openatt/paper
make pdf TECTONIC=/path/to/tectonic PYTHON=/path/to/python
```

Run the benchmark first to collect new measurements. `scripts/verify_evidence.py`
checks that recorded measurements match the current measured source files.
Generated-image/trace trials are local and synthetic; no hardware, LLM evaluation,
physical relay, external interoperability, formal proof or new cryptography is
asserted. The typed-policy control matches the serial decisions. A broad
composition/acquisition contribution remains proposed research.
