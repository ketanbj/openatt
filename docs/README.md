# OPENATT documentation

OpenATT processes force/time samples, checks a public contact pattern and signs
a controller report. A separate owner grant supplies permission for the action.

| Goal | Read next |
|---|---|
| Understand the contact/permission boundary | [Project README](../README.md) |
| Find the signal or signing code | [Code map](code-map.md) |
| Install, change code, run checks | [Development guide](development.md) |
| Inspect units, thresholds and capture assumptions | [Architecture](architecture.md), [threat model](threat-model.md) |
| Inspect generated-signal measurements | [Recorded benchmarks](benchmarks/README.md), [environment](benchmarks/environment.json) |
| Assess prior work and limits | [Novelty boundaries](novelty.md) |
| Read or rebuild the manuscript | [Paper guide](../paper/README.md) |
| Work as a coding agent | [Agent instructions](../AGENTS.md) |

## Read with these boundaries

The CLI demo and public fixtures are local and generated. Runtime behavior is
implemented in `src/`; numeric evidence comes from the raw report under
`docs/benchmarks/`. Research targets and stronger physical guarantees are described
as future work. A receipt is a local database record of an accepted request.

The shared core is maintained in the separate OpenModalityTrust repository.
OpenAVT's voice protocol remains independent of this local profile.
