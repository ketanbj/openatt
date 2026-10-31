"""SDK example: generated contact evidence; permission is a separate owner grant."""

import tempfile
from pathlib import Path

from modality_trust import Action, Contract, Gateway, Signer, grant

from openatt import read_csv, respond, simulate, write_csv

now = 1000000  # synthetic demo clock
controller, owner = Signer.generate("controller"), Signer.generate("owner")
action = Action("agent", "record-fixture-contact", "fixture/1", "fixture-test", {})
with tempfile.TemporaryDirectory() as directory:
    gateway = Gateway(
        str(Path(directory) / "state.sqlite3"),
        audience="business",
        attesters={"controller": controller.public_key},
        delegators={"owner": owner.public_key},
        clock=lambda: now,
    )
    challenge = gateway.challenge(action, "tactile")
    path = Path(directory) / "generated.csv"
    write_csv(path, simulate(challenge))
    evidence = respond(controller, challenge, action, read_csv(path), now=now)
    permission = grant(owner, action, "business", now=now, modalities=("tactile",))
    gateway.register_grant(permission)
    print(gateway.commit(evidence, permission, action, Contract("tactile")))
