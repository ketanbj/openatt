"""Check recorded benchmark arithmetic and the exact measured source hashes."""

import hashlib
import json
from pathlib import Path

import modality_trust

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "docs/benchmarks/local-2026-10-31.json").read_text())
for relative, expected in data["environment"]["source_sha256"].items():
    if relative.startswith("src/modality_trust/"):
        path = Path(modality_trust.__file__).parents[1] / relative.removeprefix("src/")
    else:
        path = ROOT / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"Measured source changed: {relative}; rerun benchmark and report")
security = data["security"]
rows = security["rows"]
assert len(rows) == security["observations"] == security["cases_per_trial"] * security["repetitions"]
assert all(row["accepted"] == row["expected"] == row["typed_reference"] for row in rows)
assert all(row["new_effects"] == int(row["expected"]) for row in rows)
channel = data.get("channel", data.get("signal"))
assert len(channel["rows"]) == channel["observations"]
for key, result in channel["summary"].items():
    if "channel" in data:
        subset = [r for r in channel["rows"] if r["condition"] == key]
        successes = sum(r["success"] for r in subset)
        assert successes == result["successes"]
    else:
        noise, jitter = (int(part.split("=")[1]) for part in key.split(","))
        subset = [r for r in channel["rows"] if r["noise_mn"] == noise and r["duration_jitter_ms"] == jitter]
        assert sum(r["accepted"] for r in subset) == result["accepted"]
    assert len(subset) == result["trials"]
print(f"{ROOT.name}: benchmark arithmetic and measured source hashes verified")
