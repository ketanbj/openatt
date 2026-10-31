#!/usr/bin/env python3
"""Regenerate tables/figures exclusively from the recorded local JSON report."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NAME = "openatt"
REPORT = ROOT / "docs/benchmarks/local-2026-10-31.json"


def tex(value):
    return str(value).replace("_", r"\_").replace("%", r"\%").replace("&", r"\&")


def main():
    data = json.loads(REPORT.read_text())
    artifacts = ROOT / "paper/artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    security = data["security"]
    macros = {
        "BenchTrials": security["repetitions"],
        "SecurityCases": security["cases_per_trial"],
        "SecurityObservations": security["observations"],
        "UnauthorizedEffects": security["unauthorized_new_effects"],
        "TypedDisagreements": security["typed_reference_disagreements"],
        "SignatureFalseAccepts": security["signature_only_false_accepts"],
        "GateMedian": f"{security['cost']['median_ms']:.3f}",
        "GatePninetyfive": f"{security['cost']['p95_ms']:.3f}",
    }
    channel = data["channel"] if NAME == "openast" else data["signal"]
    macros["ChannelObservations"] = channel["observations"]
    if NAME == "openast":
        macros["CleanSuccesses"] = channel["summary"]["clean"]["successes"]
        macros["CleanMedian"] = f"{channel['summary']['clean']['decode_cost']['median_ms']:.3f}"
        macros["CleanPninetyfive"] = f"{channel['summary']['clean']['decode_cost']['p95_ms']:.3f}"
    else:
        macros["CleanSuccesses"] = channel["summary"]["noise=0,jitter=0"]["accepted"]
        macros["PatternCollisions"] = data["limitations"]["old_trace_pattern_matches"]
        macros["CollisionTrials"] = data["limitations"]["different_challenges"]
    (artifacts / "measurements.tex").write_text(
        "% Generated from raw benchmark JSON; do not edit.\n"
        + "\n".join(
            chr(92) + "newcommand{" + chr(92) + key + "}{" + str(value) + "}" for key, value in macros.items()
        )
        + "\n"
    )
    lines = [
        f"# {NAME.upper()} local benchmark evidence",
        "",
        "Generated from `local-2026-10-31.json`; synthetic channel trials, not deployment results.",
        "",
        f"Report SHA-256: `{hashlib.sha256(REPORT.read_bytes()).hexdigest()}`.",
        "",
        "## Reproduce",
        "",
        "```sh",
        f"python {NAME}/scripts/benchmark.py --trials 20",
        f"python {NAME}/scripts/report.py",
        "```",
        "",
        "Install the local shared core and modality package first, plus pytest, matplotlib and (for OpenAST) opencv-python-headless.",
        "",
        "New runs use fresh signing keys and random security challenges; image outcomes and timing may vary.",
        "The signal scenario seeds are explicit. Code SHA-256s, environment versions, per-case outcomes and timings are in the JSON.",
        "",
        "## Channel results",
        "",
        "| Condition | Successes | 95% Wilson interval | Median / p95 processing (ms) |",
        "|---|---:|---:|---:|",
    ]
    table = [r"\begin{tabular}{lrr}", r"\toprule", r"Condition & Accepted & Median ms \\", r"\midrule"]
    for condition, row in channel["summary"].items():
        success = row.get("successes", row.get("accepted"))
        cost = row.get("decode_cost", row.get("processing_cost"))
        low, high = row["wilson95"]
        lines.append(
            f"| {condition} | {success}/{row['trials']} | {low:.3f}-{high:.3f} | {cost['median_ms']:.3f} / {cost['p95_ms']:.3f} |"
        )
        table.append(f"{tex(condition)} & {success}/{row['trials']} & {cost['median_ms']:.3f}" + r" \\")
    table += [r"\bottomrule", r"\end{tabular}"]
    (artifacts / "channel-table.tex").write_text("\n".join(table) + "\n")
    lines += [
        "",
        "Conditions are paired within each source-image/scenario trial. Wilson intervals are descriptive per-condition binomial intervals, not independent evidence across paired conditions or estimates of real-world security.",
        "",
        "## Exact-action policy cases",
        "",
        f"{security['observations']} observations ({security['cases_per_trial']} cases x {security['repetitions']} trials).",
        "",
        "| Case | Gateway accepted | Signature-only accepted | Typed control accepted | New effects |",
        "|---|---:|---:|---:|---:|",
    ]
    for case in dict.fromkeys(row["case"] for row in security["rows"]):
        subset = [r for r in security["rows"] if r["case"] == case]
        lines.append(
            f"| {case} | {sum(r['accepted'] for r in subset)} | {sum(r['signature_only'] for r in subset)} | {sum(r['typed_reference'] for r in subset)} | {sum(r['new_effects'] for r in subset)} |"
        )
    lines += [
        "",
        f"Unexpected outcomes: {security['unexpected_outcomes']}; unauthorized **new local receipts**: {security['unauthorized_new_effects']}; disagreements with the typed control: {security['typed_reference_disagreements']}.",
        "",
        f"Gate processing over mixed accepted/denied cases: median {security['cost']['median_ms']:.3f} ms, p95 {security['cost']['p95_ms']:.3f} ms. This is not an end-to-end physical-channel delay.",
        "",
        "The signature-only baseline intentionally ignores action permission and freshness. Its failures are an ablation, not evidence against a fully scoped existing authorization system. The typed control has the same serial policy and shares crypto/adapter primitives; no security advantage over it is demonstrated.",
        "",
        "The relay and compromised-attester cases forward valid structured bytes; they are **modeled limitations**, not measured physical attacks. They are accepted only when proximity/sensor truth is not required. Separate proximity/consent requirements are denied.",
        "",
        "The policy attack cases enter after modality decoding; the channel and policy suites are separate. The end-to-end demos combine both paths.",
        "",
        "## Concurrency",
        "",
        f"{data['concurrency']['trials']} trials each of {data['concurrency']['workers']} simultaneous duplicate attempts and revocation serialized before commit. Each duplicate trial produces exactly one receipt; each prior-revocation trial produces zero. State is a local SQLite file, not a remote or physical actuator.",
        "",
    ]
    if NAME == "openatt":
        limits = data["limitations"]
        lines += [
            "## Short-pattern negative result",
            "",
            f"An old trace matched {limits['old_trace_pattern_matches']}/{limits['different_challenges']} different challenge patterns. The 8-bit code space has 256 patterns. This is not authentication: a trusted capture path and full signed nonce/session binding remain required.",
            "",
        ]
    lines += [
        "## Limits",
        "",
        "Generated fixtures contain no human subjects or customer data. No camera/display hardware, force sensor, LLM, live relay, cloud integration, formal proof or independent security review was evaluated. Timings are one-host descriptive measurements; do not pool trial repetitions into a deployment security claim.",
        "",
    ]
    (ROOT / "docs/benchmarks/README.md").write_text("\n".join(lines))
    plt.rcParams.update({"font.size": 9, "font.family": "DejaVu Sans"})
    if NAME == "openast":
        labels = list(channel["summary"])
        successes = np.array(
            [channel["summary"][k]["successes"] / channel["summary"][k]["trials"] for k in labels]
        )
        low = np.array([channel["summary"][k]["wilson95"][0] for k in labels])
        high = np.array([channel["summary"][k]["wilson95"][1] for k in labels])
        fig, ax = plt.subplots(figsize=(6.4, 4.8), layout="constrained")
        ax.errorbar(
            successes,
            np.arange(len(labels)),
            xerr=[np.maximum(0, successes - low), np.maximum(0, high - successes)],
            fmt="o",
            color="#135e77",
            capsize=3,
        )
        ax.set_yticks(np.arange(len(labels)), labels)
        ax.invert_yaxis()
        ax.set_xlim(-0.05, 1.05)
        ax.set_xlabel("Exact-byte decode fraction (generated rasters)")
        ax.grid(axis="x", alpha=0.2)
    else:
        values = np.array(
            [
                [
                    channel["summary"][f"noise={noise},jitter={jitter}"]["accepted"]
                    / channel["summary"][f"noise={noise},jitter={jitter}"]["trials"]
                    for jitter in (0, 10, 30)
                ]
                for noise in (0, 100, 300, 600)
            ]
        )
        fig, ax = plt.subplots(figsize=(5.4, 3.5), layout="constrained")
        image = ax.imshow(values, vmin=0, vmax=1, cmap="Blues", aspect="auto")
        ax.set_xticks(range(3), ["0", "10", "30"])
        ax.set_yticks(range(4), ["0", "100", "300", "600"])
        ax.set_xlabel("Uniform contact-duration jitter bound (ms)")
        ax.set_ylabel("Uniform force-noise bound (mN)")
        for i in range(4):
            for j in range(3):
                ax.text(
                    j,
                    i,
                    f"{values[i, j]:.0%}",
                    ha="center",
                    va="center",
                    color="white" if values[i, j] > 0.5 else "black",
                )
        fig.colorbar(image, ax=ax, label="Pattern acceptance (generated traces)")
    fig.savefig(artifacts / "channel.pdf")
    fig.savefig(artifacts / "channel.png", dpi=180)
    plt.close(fig)
    print(f"Generated tables, figure and benchmark README from {REPORT}")


if __name__ == "__main__":
    main()
