# Tests

Run `python -m pytest tests` from this repository after installing the package
and its local shared core. Tests cover the actual modality parser and protocol.
The umbrella `core/tests` adds permission, replay, transaction, concurrency and
unsupported-guarantee cases. Benchmark runners record separate raw measurements.
