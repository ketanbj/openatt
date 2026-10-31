# OPENATT: Open Agent Tactile Trust

**Exploratory tactile research scaffold.** Part of [OpenModalityTrust](https://github.com/ketanbj/open-modality-trust).

This repository will explore signed controller reports, contact/haptic challenges and the distinction between contact and consent.

There is no implemented security protocol or runnable adapter yet. The current
repository contains design boundaries and the intended source/test/example
structure. A signed sensor report identifies a reporting controller under configured trust. It does not establish the toucher's identity, intention or human consent.

The common contracts live in the umbrella's `spec/` directory. They are drafts,
not wire-level interoperability guarantees. The umbrella pins this repository
as a submodule under `modalities/openatt`. Contribute here independently, publish
child commits, then update the umbrella pointer.

- [Design](docs/design.md)
- [Source scope](src/openatt/README.md)
- [Test plan](tests/README.md)
- [Example plan](examples/README.md)
