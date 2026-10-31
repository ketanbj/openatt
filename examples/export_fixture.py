"""Export an explicitly synthetic public fixture; private keys are never written."""

import json
from pathlib import Path

from modality_trust import Action, Signer, unpack

from openatt import respond, simulate, write_csv

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fixtures"
OUT.mkdir(exist_ok=True)

action = Action("fixture-agent", "record", "fixture/42", "fixture", {})
signer = Signer.generate("fixture-controller")
challenge = dict(
    v=1,
    audience="fixture-backend",
    modality="tactile",
    nonce="synthetic-tactile-nonce",
    session="synthetic-tactile-session",
    request_digest=action.digest,
    issued_at=1000,
    expires_at=1030,
)
samples = simulate(challenge, seed=42, noise_mn=100)
evidence = respond(signer, challenge, action, samples, now=1000)
write_csv(OUT / "generated-trace.csv", samples)
(OUT / "public.json").write_text(
    json.dumps(
        {
            "synthetic": True,
            "measurement_trial": False,
            "public_key_hex": signer.public_key.hex(),
            "action": action.document,
            "evidence": unpack(evidence),
        },
        indent=2,
    )
    + "\n"
)
