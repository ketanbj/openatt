import argparse
import json
import tempfile
import time
from pathlib import Path

from modality_trust import Action, Contract, Denied, Gateway, Signer, grant

from .protocol import respond
from .trace import analyze, pattern, read_csv, simulate, write_csv


def demo(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    controller, owner = Signer.generate("controller.demo"), Signer.generate("owner.demo")
    action = Action("agent.demo", "record-fixture-contact", "fixture/demo-1", "fixture-test", {})
    with tempfile.TemporaryDirectory(prefix="openatt-") as temporary:
        gateway = Gateway(
            str(Path(temporary) / "state.sqlite3"),
            audience="fixture.demo",
            attesters={"tactile": {controller.issuer: controller.public_key}},
            delegators={owner.issuer: owner.public_key},
        )
        challenge = gateway.challenge(action, "tactile")
        samples = simulate(challenge, seed=42)
        path = directory / "simulated-trace.csv"
        write_csv(path, samples)
        evidence = respond(controller, challenge, action, read_csv(path), now=int(time.time()))
        permission = grant(owner, action, gateway.audience, now=int(time.time()), modalities=("tactile",))
        gateway.register_grant(permission)
        # Requiring consent must fail even when all tactile checks succeed.
        try:
            gateway.commit(
                evidence,
                permission,
                action,
                Contract("tactile", required_guarantees=frozenset({"human-consent"})),
            )
        except Denied as error:
            consent = str(error)
        else:
            raise RuntimeError("contact was unexpectedly promoted to consent")
        receipt = gateway.commit(evidence, permission, action, Contract("tactile"))
        report = {
            "receipt": receipt,
            "consent_requirement": consent,
            "effects": len(gateway.effects()),
            "pattern_ms": pattern(challenge),
            "contacts": analyze(samples),
            "source": "generated force/time CSV",
            "hardware_trial": False,
        }
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description="OpenATT experimental tactile controller evidence")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("demo")
    run.add_argument("--output", type=Path, default=Path("output/demo"))
    inspect = commands.add_parser("inspect", help="inspect contact segments; does not authenticate the CSV")
    inspect.add_argument("trace", type=Path)
    args = parser.parse_args()
    if args.command == "demo":
        print(json.dumps(demo(args.output), indent=2))
    else:
        print(json.dumps({"contacts": analyze(read_csv(args.trace)), "authenticated": False}, indent=2))
