import copy

import pytest
from modality_trust import Action, Contract, Denied, Gateway, Signer, grant

from openatt import analyze, read_csv, respond, simulate, write_csv
from openatt.trace import pattern, validate_pattern


@pytest.fixture
def fixture(tmp_path):
    controller, owner = Signer.generate("controller"), Signer.generate("owner")
    action = Action("agent", "record", "fixture/1", "fixture-test", {})
    gateway = Gateway(
        str(tmp_path / "state.sqlite3"),
        audience="backend",
        attesters={"controller": controller.public_key},
        delegators={"owner": owner.public_key},
        clock=lambda: 1000,
    )
    challenge = gateway.challenge(action, "tactile")
    return controller, owner, action, gateway, challenge


def test_trace_roundtrip_and_signed_commit(tmp_path, fixture):
    controller, owner, action, gateway, challenge = fixture
    samples = simulate(challenge, seed=7, noise_mn=100)
    path = tmp_path / "capture.csv"
    write_csv(path, samples)
    assert read_csv(path) == samples
    evidence = respond(controller, challenge, action, read_csv(path), now=1000)
    permission = grant(owner, action, "backend", now=1000)
    gateway.register_grant(permission)
    receipt = gateway.commit(evidence, permission, action, Contract("tactile"))
    assert "reported-contact" in receipt["guarantees"]
    assert "human-consent" not in receipt["guarantees"]


def test_contact_never_becomes_consent(fixture):
    controller, owner, action, gateway, challenge = fixture
    evidence = respond(controller, challenge, action, simulate(challenge), now=1000)
    permission = grant(owner, action, "backend", now=1000)
    gateway.register_grant(permission)
    with pytest.raises(Denied, match="unsupported-guarantee"):
        gateway.commit(evidence, permission, action, Contract("tactile", frozenset({"human-consent"})))
    assert not gateway.effects()


@pytest.mark.parametrize(
    "mutation", ["gap", "reverse", "negative", "float", "bool", "unfinished", "spike", "count"]
)
def test_acquisition_quality(fixture, mutation):
    *_, challenge = fixture
    samples = copy.deepcopy(simulate(challenge))
    if mutation == "gap":
        del samples[5:10]
    elif mutation == "reverse":
        samples[5][0] = samples[4][0]
    elif mutation == "negative":
        samples[5][1] = -1
    elif mutation == "float":
        samples[5][1] = 1.5
    elif mutation == "bool":
        samples[5][0] = True
    elif mutation == "unfinished":
        samples[-1][1] = 1000
    elif mutation == "spike":
        samples[1][1] = 1000
    else:
        samples = samples * 4
    with pytest.raises(ValueError):
        analyze(samples)


def test_pattern_binding_detects_a_different_code(fixture):
    *_, challenge = fixture
    other = {**challenge, "nonce": "other"}
    while pattern(other) == pattern(challenge):
        other["nonce"] += "x"
    with pytest.raises(ValueError, match="pattern"):
        validate_pattern(simulate(other), challenge)


def test_eight_bit_patterns_can_collide_and_are_not_authentication(fixture):
    *_, challenge = fixture
    target = pattern(challenge)
    # Pigeonhole demonstration: eight tactile bits do not carry cryptographic freshness.
    seen = {}
    for index in range(257):
        candidate = {**challenge, "nonce": str(index)}
        code = tuple(pattern(candidate))
        if code in seen:
            assert candidate != seen[code]
            break
        seen[code] = candidate
    else:
        pytest.fail("257 candidates must collide in a 256-code space")
    assert len(target) == 8


def test_csv_shape_and_units(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("time,force\n0,0\n")
    with pytest.raises(ValueError):
        read_csv(path)
