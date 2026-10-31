# Develop OPENATT

All commands below run from **this repository root**, after activating a Python
3.11+ virtual environment. Use `make help` to inspect commands before running them.

## Install in either checkout layout

| Layout | Shared core path relative to this repository |
|---|---|
| Standalone repository beside an umbrella checkout | `../open-modality-trust/core` |
| Recursive umbrella checkout under `modalities/openatt` | `../../core` |
| Any other layout | Supply `CORE=/absolute/path/to/core` |

If the umbrella is missing from a standalone checkout, obtain its source first:

```sh
git clone https://github.com/ketanbj/open-modality-trust.git ../open-modality-trust
```

Skip that clone if the sibling directory already exists. Then:

```sh
python3 -m venv .venv
source .venv/bin/activate
make install
make check
make demo
```

`make install` checks the shared package's identity and installs it plus this
adapter and developer tools from source. It detects the two layouts above.
Override the interpreter with `PYTHON=/path/to/python` if needed. Without Make,
the sibling-layout equivalent is:

```sh
python -m pip install -e ../open-modality-trust/core -e '.[dev]'
python -m pytest -q tests
python scripts/check_docs.py
```

For a shared-core change, install both adapters into the same environment and
run the umbrella's complete test suite. This adapter's tests alone do not cover
all shared permission/transaction behavior.

## Choose the smallest useful check

| Changed area | Check |
|---|---|
| Documentation/navigation | `make check-docs` and review the wording/commands |
| Adapter parser/protocol | Closest tests, then `make check` |
| CLI/demo | `make demo` plus relevant tests |
| Package/dependency configuration | `make build` and an installed-wheel smoke run |
| Recorded evidence or manuscript | The evidence/publication workflow below |

`make build DIST=output/fresh-dist` keeps comparison archives separate from
previous builds.

`make check` runs lint, format checks, local documentation links, adapter tests
and recorded-evidence verification. It does not call a model API, use hardware,
run a new benchmark or rebuild publication artifacts.

## Run new measurements without replacing recorded evidence

```sh
make install-benchmark
make benchmark TRIALS=20 OUT=output/benchmark/new-run.json
make verify-evidence
```

The optional benchmark extra installs plot/transform dependencies. The Make
wrapper supplies `--output`, so new runs go to ignored `output/`. The original
benchmark script's default path is the tracked historical report: supply an
explicit output when exploring. `make verify-evidence` checks the recorded
source hashes and arithmetic, not the new report.

If measured implementation files changed, the historical source check should
report a mismatch. Preserve that history. Review a new run and record an explicit
evidence update; do not edit hashes or conclusions to make a check pass.

The dated generated benchmark page uses commands relative to the parent family
directory (`python openatt/scripts/...`). The Make commands above consistently
run from this repository root.

## Update publication artifacts deliberately

The current report generator reads the canonical tracked report at
`docs/benchmarks/local-2026-10-31.json`. It does not read the Make benchmark's
ignored output automatically. A new publication snapshot needs a reviewed decision
about its source/report path and retention of the previous snapshot.

For the already recorded snapshot, `make report` regenerates the benchmark README,
LaTeX numbers and plots. `make paper TECTONIC=/path/to/tectonic` also compiles the
paper. Both modify tracked publication files. Re-render and inspect the resulting
PDF, refresh the artifact hash/review record to the actual inspected files, and
review the complete diff before publishing. Documentation-only work does not
need these commands.

## Common problems

| Symptom | What to do |
|---|---|
| Shared core cannot be found | Set `CORE` to the umbrella's `core/` path |
| CSV rejected | Use the exact `time_ms,force_mn` header and integer milliseconds/millinewtons; check gaps, ordering and force bounds |
| Trace looks like contact but pattern fails | Contact segmentation and challenge-pattern matching are separate checks; inspect the failure reason |
| A different challenge accepts an old raw pattern | Eight bits allow collisions; the full signed challenge and trusted capture ordering are separate requirements |
| Human-consent requirement is denied | This is the expected boundary; contact cannot supply that guarantee |
| Evidence source hash differs | Review the changed file and follow the evidence-update workflow |


## Publish repository changes

This repository has its own history. Publish the child commit before updating
its exact submodule pointer in the umbrella; see the umbrella's development guide.
Use the [code map](code-map.md) for source/generated-file ownership and
[agent guide](../AGENTS.md) for a compact task checklist.
