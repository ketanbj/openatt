# Contribute to OPENATT

Start with the [documentation map](docs/README.md), then follow the
[development guide](docs/development.md) for your checkout layout. Coding agents
should also read [AGENTS.md](AGENTS.md).

1. Find the owning module and closest tests in the [code map](docs/code-map.md).
2. Make the requested change; describe any changed guarantees or assumptions in
   the architecture/threat model and appropriate tests.
3. Use `make check-docs` for documentation-only changes, or the focused checks in
   the development guide for code, packaging or evidence changes.
4. Keep measurements and proposed capabilities distinct. Preserve historical
   benchmark reports; new exploratory runs belong in ignored `output/`.
5. Publish this repository's commit before updating its umbrella submodule pin.

Code is Apache-2.0. Public fixtures must be synthetic or have documented rights.
Keep private keys, credentials, grants, databases and unconsented recordings out
of commits. Rebuilding a paper requires visual review and matching artifact hashes.
