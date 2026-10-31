# OPENATT: Open Agent Tactile Trust

**A signed contact report with a clear boundary between touch and permission.**

An assistant receives a button-contact report. OpenATT lets a configured
controller sign bounded force/time samples for an exact interaction. A separate
owner grant supplies permission; contact itself cannot approve the action.

[Documentation map](docs/README.md) · [Code map](docs/code-map.md) ·
[Development](docs/development.md) · [Agent guide](AGENTS.md)

## What works today

Bounded CSV acquisition, integer force/time processing, contact segmentation,
challenge-pattern appraisal, signed controller reports and shared permission/local
receipt enforcement.
The prototype ends by writing a **local receipt**: a database record of an
accepted request. Remote business actions and actuators need their own
participating effect boundary.

The released traces are generated simulations. Sensor truth, capture ordering,
toucher identity, human consent and proximity require additional justified
evidence/assumptions. No physical sensor or LLM agent study was performed.

## Run from this repository root

Requires Python 3.11+. The shared core source must be available in the umbrella
checkout. If you cloned this repository independently, place the umbrella beside
it, or pass its core path explicitly. Skip the following clone if it already exists:

```sh
git clone https://github.com/ketanbj/open-modality-trust.git ../open-modality-trust
```

Then, from **this repository root**:

```sh
python3 -m venv .venv
source .venv/bin/activate
make install
make demo
make check
```

The installer detects sibling and recursive-umbrella layouts. For any other
layout, use `make install CORE=/absolute/path/to/core`. All packages come from
local source; no PyPI publication is asserted. The demo uses generated inputs and
ephemeral keys, with no API key, cloud account or hardware.

The [development guide](docs/development.md) includes direct Python commands if
you do not use Make, plus setup and troubleshooting for both checkout layouts.

## Understand the path to a permitted receipt

1. The verifier stores a fresh challenge for the exact principal, action,
   resource, purpose and arguments.
2. A configured controller signs the challenge and bounded force trace; the verifier recomputes the contact pattern.
3. A separate owner key issues a grant for that action and business audience.
4. The shared gateway checks supported guarantees, current permission, expiry,
   revocation and one-use state before committing the receipt in one transaction.

Inspecting CSV returns contact segments; it does not authenticate the capture.

```sh
python -m openatt inspect examples/fixtures/generated-trace.csv
```

The signed [public fixture](examples/fixtures/README.md) is synthetic and separate
from measured benchmark trials. Its public key is a fixture verification key,
not a production trust root. The [SDK example](examples/workflow.py) shows how
observation signing, owner permission and the gateway fit together.

## Inspect and reproduce evidence

- [Recorded benchmarks](docs/benchmarks/README.md): raw results, controls and failures.
- [Measured environment](docs/benchmarks/environment.json): versions for the recorded run.
- [Architecture](docs/architecture.md) and [threat model](docs/threat-model.md): exact scope and assumptions.
- [Research position](docs/novelty.md) and [paper guide](paper/README.md): prior work and manuscript sources.

```sh
make install-benchmark
make benchmark TRIALS=20 OUT=output/benchmark/new-run.json
make verify-evidence
```

New exploratory runs go to ignored output paths. `verify-evidence` checks the
recorded report and measured source files. The [publication workflow](docs/development.md#update-publication-artifacts-deliberately)
explains deliberate updates to recorded tables, plots and reviewed PDFs.

The sequential reference checker with the same policy matches the recorded
permission decisions. These local results establish an inspectable experimental
reference, with explicit limits. Signatures, visual/haptic authentication and
transactions are established techniques; broader composition and acquisition
benefits remain research, not measured advantages of this prototype.

See [CONTRIBUTING.md](CONTRIBUTING.md) to make changes. Code is Apache-2.0;
fixtures contain no people, customer records or private keys.
