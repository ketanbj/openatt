# OPENATT tests

From this repository root after [setup](../docs/development.md):

```sh
make test
```

The adapter tests cover its actual parser/protocol and the committed public
synthetic fixture. Shared grant, role separation, revocation, replay, rollback and
concurrency behavior is covered by `core/tests` in the umbrella. Use the umbrella's
`make test` after a shared-core change. Tests and benchmark measurements serve
different purposes; see [recorded evidence](../docs/benchmarks/README.md).
