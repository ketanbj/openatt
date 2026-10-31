# OPENATT examples

Run from this repository root after the [development setup](../docs/development.md).

| Example | Command | Meaning |
|---|---|---|
| End-to-end local demo | `make demo` | Generated input, separate owner permission, accepted local receipt |
| Small SDK workflow | `python examples/workflow.py` | Public API without CLI orchestration |
| Committed public fixture | See [fixtures](fixtures/README.md) | Inspectable synthetic input and signature/public key |
| Fixture exporter | `python examples/export_fixture.py` | Replaces public fixture files with a fresh synthetic instance; run only for an intentional fixture update |

These examples do not run hardware, identify a consenting person or deploy a
business backend. The [code map](../docs/code-map.md) separates example code,
measured reports and generated publication artifacts.
