# OPENATT code and artifact map

| File | Responsibility | Useful verification |
|---|---|---|
| [trace.py](../src/openatt/trace.py) | `read_csv`, `analyze`, `validate_pattern`; bounded integer units, contact segmentation and quality checks; `simulate` generates test data | `tests/test_tactile.py` |
| [protocol.py](../src/openatt/protocol.py) | `respond` signs the challenge/trace; `appraise` independently checks resource, profile and pattern | `tests/test_tactile.py`; shared core tests |
| [cli.py](../src/openatt/cli.py) | Local demo and unauthenticated CSV inspection | `make demo` |
| [workflow.py](../examples/workflow.py) | SDK example with separate controller and owner keys | Run `python examples/workflow.py` |
| [public fixture](../examples/fixtures/README.md) | Generated CSV, signed report and public verification key | `tests/test_tactile_fixture.py` |
| [benchmark.py](../scripts/benchmark.py) | Generated noise/jitter cases, policy checks, concurrency and pattern-collision experiment | `make benchmark` |
| [verify_evidence.py](../scripts/verify_evidence.py) | Recorded arithmetic and measured source hashes | `make verify-evidence` |
| [report.py](../scripts/report.py) | Benchmark prose, LaTeX measurements and plots derived from recorded JSON | Publication workflow below |

## Shared enforcement

The separately installed `modality_trust` package owns immutable actions,
per-modality issuer trust, owner grants, revocation/replay state and transactional
local receipts. The implementation lives in the umbrella's
`core/src/modality_trust/`; its main behavior tests are `core/tests/test_core.py`.
An adapter change does not automatically update the shared core or other adapters.

## Editable sources and generated evidence

- Edit `src/`, `tests/`, human guides and Makefiles for implementation/navigation work.
- `examples/fixtures/` contains public synthetic inputs; its exporter writes fresh
  random keys/signatures, so do not regenerate it for unrelated documentation edits.
- `docs/benchmarks/local-2026-10-31.json` is a recorded measurement snapshot.
- `docs/benchmarks/README.md`, `paper/artifacts/measurements.tex` and channel plots
  are generated from that snapshot by `scripts/report.py`.
- `paper/sections/` and `paper/references.bib` are editable manuscript sources.
- Compiled PDFs and `paper/artifacts/build-verification.json` identify the reviewed
  build. Rebuilding a PDF alone does not refresh its review/hashes.

See [development](development.md) before updating evidence or publication files.
