# OPENATT local benchmark evidence

Generated from `local-2026-10-31.json`; synthetic channel trials, not deployment results.

Report SHA-256: `cc86ad7f8f8b67914af706b4bc85e5b064fedd5606aa688fc65f3c11c63555db`.

## Reproduce

```sh
python openatt/scripts/benchmark.py --trials 20
python openatt/scripts/report.py
```

Install the local shared core and modality package first, plus pytest, matplotlib and (for OpenAST) opencv-python-headless.

New runs use fresh signing keys and random security challenges; image outcomes and timing may vary.
The signal scenario seeds are explicit. Code SHA-256s, environment versions, per-case outcomes and timings are in the JSON.

## Channel results

| Condition | Successes | 95% Wilson interval | Median / p95 processing (ms) |
|---|---:|---:|---:|
| noise=0,jitter=0 | 20/20 | 0.839-1.000 | 0.408 / 0.574 |
| noise=0,jitter=10 | 20/20 | 0.839-1.000 | 0.406 / 0.486 |
| noise=0,jitter=30 | 3/20 | 0.052-0.360 | 0.126 / 0.383 |
| noise=100,jitter=0 | 20/20 | 0.839-1.000 | 0.412 / 0.452 |
| noise=100,jitter=10 | 20/20 | 0.839-1.000 | 0.406 / 0.428 |
| noise=100,jitter=30 | 3/20 | 0.052-0.360 | 0.118 / 0.474 |
| noise=300,jitter=0 | 18/20 | 0.699-0.972 | 0.405 / 0.481 |
| noise=300,jitter=10 | 20/20 | 0.839-1.000 | 0.405 / 0.452 |
| noise=300,jitter=30 | 4/20 | 0.081-0.416 | 0.118 / 0.431 |
| noise=600,jitter=0 | 0/20 | 0.000-0.161 | 0.058 / 0.080 |
| noise=600,jitter=10 | 0/20 | 0.000-0.161 | 0.058 / 0.078 |
| noise=600,jitter=30 | 0/20 | 0.000-0.161 | 0.056 / 0.064 |

Conditions are paired within each source-image/scenario trial. Wilson intervals are descriptive per-condition binomial intervals, not independent evidence across paired conditions or estimates of real-world security.

## Exact-action policy cases

640 observations (32 cases x 20 trials).

| Case | Gateway accepted | Signature-only accepted | Typed control accepted | New effects |
|---|---:|---:|---:|---:|
| valid | 20 | 20 | 20 | 20 |
| evidence-tamper | 0 | 0 | 0 | 0 |
| unconfigured-key | 0 | 0 | 0 | 0 |
| action-substitution | 0 | 20 | 0 | 0 |
| resource-substitution | 0 | 20 | 0 | 0 |
| principal-substitution | 0 | 20 | 0 | 0 |
| purpose-substitution | 0 | 20 | 0 | 0 |
| arguments-substitution | 0 | 20 | 0 | 0 |
| session-transplant | 0 | 20 | 0 | 0 |
| nonce-transplant | 0 | 20 | 0 | 0 |
| wrong-audience | 0 | 20 | 0 | 0 |
| expired-challenge | 0 | 20 | 0 | 0 |
| expired-grant | 0 | 20 | 0 | 0 |
| revoked-grant | 0 | 20 | 0 | 0 |
| revoked-before-registration | 0 | 20 | 0 | 0 |
| revoked-attester | 0 | 20 | 0 | 0 |
| revoked-delegator | 0 | 20 | 0 | 0 |
| unregistered-grant | 0 | 20 | 0 | 0 |
| wrong-grant-scope | 0 | 20 | 0 | 0 |
| wrong-grant-modality | 0 | 20 | 0 | 0 |
| wrong-attester-modality | 0 | 0 | 0 | 0 |
| consumed-replay | 0 | 20 | 0 | 0 |
| unknown-observation-profile | 0 | 20 | 0 | 0 |
| extra-observation-field | 0 | 20 | 0 | 0 |
| unaccepted-assumption | 0 | 20 | 0 | 0 |
| require-proximity | 0 | 20 | 0 | 0 |
| require-consent | 0 | 20 | 0 | 0 |
| fresh-relay-without-proximity-requirement | 20 | 20 | 20 | 20 |
| compromised-attester-without-sensor-truth-requirement | 20 | 20 | 20 | 20 |
| trace-gap | 0 | 20 | 0 | 0 |
| trace-force-substitution | 0 | 20 | 0 | 0 |
| wrong-pattern | 0 | 20 | 0 | 0 |

Unexpected outcomes: 0; unauthorized **new local receipts**: 0; disagreements with the typed control: 0.

Gate processing over mixed accepted/denied cases: median 0.498 ms, p95 1.688 ms. This is not an end-to-end physical-channel delay.

The signature-only baseline intentionally ignores action permission and freshness. Its failures are an ablation, not evidence against a fully scoped existing authorization system. The typed control has the same serial policy and shares crypto/adapter primitives; no security advantage over it is demonstrated.

The relay and compromised-attester cases forward valid structured bytes; they are **modeled limitations**, not measured physical attacks. They are accepted only when proximity/sensor truth is not required. Separate proximity/consent requirements are denied.

The policy attack cases enter after modality decoding; the channel and policy suites are separate. The end-to-end demos combine both paths.

## Concurrency

20 trials each of 8 simultaneous duplicate attempts and revocation serialized before commit. Each duplicate trial produces exactly one receipt; each prior-revocation trial produces zero. State is a local SQLite file, not a remote or physical actuator.

## Short-pattern negative result

An old trace matched 6/1000 different challenge patterns. The 8-bit code space has 256 patterns. This is not authentication: a trusted capture path and full signed nonce/session binding remain required.

## Limits

Generated fixtures contain no human subjects or customer data. No camera/display hardware, force sensor, LLM, live relay, cloud integration, formal proof or independent security review was evaluated. Timings are one-host descriptive measurements; do not pool trial repetitions into a deployment security claim.
