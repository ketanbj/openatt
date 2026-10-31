#!/usr/bin/env python3
"""Generated force traces, signal quality, policy attacks and durable-effect races."""

import argparse
import json
import time
from pathlib import Path

import modality_trust
from modality_trust import Action, Signer
from modality_trust.benchmark import concurrency_benchmark, metadata, serial_benchmark, timing, wilson

from openatt import respond, simulate, write_csv
from openatt.trace import validate_pattern

ROOT = Path(__file__).resolve().parents[1]


def signal(trials, examples):
    rows = []
    action = Action("agent", "record", "fixture/1", "fixture-test", {})
    signer = Signer.generate("controller")
    for trial in range(trials):
        # Reproducible scenario generation; this predictable nonce is for simulation only.
        challenge = dict(
            v=1,
            audience="backend",
            modality="tactile",
            nonce=f"simulation-{trial}",
            session=f"simulation-session-{trial}",
            request_digest=action.digest,
            issued_at=1000,
            expires_at=1030,
        )
        for noise in (0, 100, 300, 600):
            for jitter in (0, 10, 30):
                samples = simulate(challenge, seed=trial, noise_mn=noise, jitter_ms=jitter)
                started = time.perf_counter_ns()
                try:
                    respond(signer, challenge, action, samples, now=1000)
                    accepted, reason = True, "pattern-matched"
                except ValueError as error:
                    accepted, reason = False, str(error)
                elapsed = (time.perf_counter_ns() - started) / 1e6
                rows.append(
                    {
                        "trial": trial,
                        "noise_mn": noise,
                        "duration_jitter_ms": jitter,
                        "accepted": accepted,
                        "reason": reason,
                        "samples": len(samples),
                        "simulated_duration_ms": samples[-1][0],
                        "processing_ms": elapsed,
                        "contact_only": any(force >= 500 for _, force in samples),
                    }
                )
                if trial == 0 and jitter == 0:
                    try:
                        write_csv(examples / f"noise-{noise}mn.csv", samples)
                    except ValueError:
                        # Malformed/quality-failing traces are still released as raw generated data.
                        import csv

                        with (examples / f"noise-{noise}mn.csv").open("w", newline="") as stream:
                            writer = csv.writer(stream)
                            writer.writerow(["time_ms", "force_mn"])
                            writer.writerows(samples)
    summary = {}
    for noise in (0, 100, 300, 600):
        for jitter in (0, 10, 30):
            subset = [r for r in rows if r["noise_mn"] == noise and r["duration_jitter_ms"] == jitter]
            successes = sum(r["accepted"] for r in subset)
            summary[f"noise={noise},jitter={jitter}"] = {
                "accepted": successes,
                "trials": trials,
                "wilson95": wilson(successes, trials),
                "processing_cost": timing([r["processing_ms"] for r in subset]),
            }
    return {
        "independent_scenarios": trials,
        "paired_conditions": 12,
        "observations": len(rows),
        "summary": summary,
        "rows": rows,
        "scope": "generated integer force/time samples; no sensor hardware",
    }


def limitations(trials=1000):
    """Demonstrate short-code collisions; no claim that an 8-bit pattern authenticates contact."""
    action = Action("agent", "record", "fixture/1", "fixture-test", {})
    base = dict(
        v=1,
        audience="backend",
        modality="tactile",
        nonce="base",
        session="session",
        request_digest=action.digest,
        issued_at=1000,
        expires_at=1030,
    )
    samples = simulate(base)
    collisions = 0
    for index in range(trials):
        different = {**base, "nonce": f"candidate-{index}"}
        try:
            validate_pattern(samples, different)
            collisions += 1
        except ValueError:
            pass
    return {
        "different_challenges": trials,
        "old_trace_pattern_matches": collisions,
        "code_space": 256,
        "expected_random_match_probability": 1 / 256,
        "interpretation": "pattern is an acquisition check; full signed nonce/session and trusted controller remain necessary",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/benchmarks/local-2026-10-31.json")
    args = parser.parse_args()
    if not 1 <= args.trials <= 1000:
        parser.error("trials must be 1..1000")
    examples = ROOT / "output/benchmark-traces"
    examples.mkdir(parents=True, exist_ok=True)
    report = {
        "profile": "openatt-local-v1",
        "environment": metadata([ROOT / "src", ROOT / "scripts", Path(modality_trust.__file__).parents[1]]),
        "signal": signal(args.trials, examples),
        "security": serial_benchmark(
            "tactile", args.trials, ("trace-gap", "trace-force-substitution", "wrong-pattern")
        ),
        "concurrency": concurrency_benchmark("tactile", args.trials),
        "limitations": limitations(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                "signal": report["signal"]["summary"],
                "security": {k: v for k, v in report["security"].items() if k != "rows"},
                "limitations": report["limitations"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
