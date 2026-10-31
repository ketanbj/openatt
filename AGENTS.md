# openatt agent guide

OpenATT signs bounded controller force/time reports and checks a public contact
pattern. The shared core verifies exact action permission and local receipts.
A controller signature does not establish truthful sensing or human consent.

## Read first

`README.md` -> `docs/README.md` -> `docs/architecture.md` -> `docs/code-map.md`.

## Commands

Run from this repository root, in a Python 3.11+ virtual environment:

```sh
make install
make help
make demo
make test
make lint
make check-docs
make verify-evidence
```

Set `CORE=/path/to/open-modality-trust/core` for a nonstandard layout.
`make install-benchmark` adds plotting dependencies. `make benchmark` writes to
ignored `output/` without replacing the recorded results. Read
`docs/development.md` before regenerating publication artifacts.

## Change map

| Change | Start with | Closest tests |
|---|---|---|
| CSV, units and contact segmentation | `src/openatt/trace.py` | `tests/test_tactile.py` |
| Signed report/context binding | `src/openatt/protocol.py` | `tests/test_tactile.py`, umbrella `core/tests` |
| CLI demo/output | `src/openatt/cli.py` | `make demo`, `tests/test_tactile_fixture.py` |
| Shared grants and local receipts | umbrella `core/src/modality_trust/gateway.py` | umbrella `core/tests/test_core.py` |
| Evidence and limitations | `scripts/benchmark.py` | recorded `docs/benchmarks/` report |

## Important boundaries

Units are integer milliseconds and millinewtons. Preserve sample bounds, monotonic
time, gap/debounce checks and profile tolerances. Eight pattern bits are a public
acquisition check, not cryptographic freshness. Capture ordering and sensor truth
remain explicit assumptions. Released traces are generated, not hardware trials.

## Working rules

- Read the task guide and closest code/tests before editing; use `rg` to navigate.
- Keep changes within the requested behavior. Explain changed guarantees in the
  architecture/threat model and cover them with relevant protocol tests.
- Preserve the separation between observations, verified claims and permission.
  Never promote a fresh signature to location, or a contact report to consent.
- Recorded benchmarks and publication artifacts are evidence. Do not hand-edit
  numeric results or overwrite historical reports to hide a mismatch. Exploratory
  benchmarks go in ignored `output/`; docs-only changes need no benchmark rerun.
- New or changed relative Markdown links should pass `make check-docs`.
- Keep keys, grants, credentials, recordings and databases out of commits. Public fixtures
  must be explicitly synthetic or have documented rights; public verification
  keys are distinct from private signing credentials.
- Publishing a package, running paid/provider integrations and submitting papers
  are separate tasks; the local demo and normal checks require none of them.
