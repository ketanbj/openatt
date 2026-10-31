import json
from pathlib import Path

from modality_trust import canonical, verify

from openatt import appraise, read_csv


def test_public_fixture_is_exact_signed_trace():
    directory = Path(__file__).resolve().parents[1] / "examples/fixtures"
    fixture = json.loads((directory / "public.json").read_text())
    protected = verify(
        canonical(fixture["evidence"]),
        {"fixture-controller": bytes.fromhex(fixture["public_key_hex"])},
        "tactile-evidence",
    )
    body = protected["body"]
    assert read_csv(directory / "generated-trace.csv") == body["observation"]["samples"]
    assert "reported-contact" in appraise(body["observation"], body["challenge"], fixture["action"])
    assert fixture["synthetic"] and not fixture["measurement_trial"]
