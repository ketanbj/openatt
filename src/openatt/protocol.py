"""A configured controller signs the captured trace and exact interaction context."""

from modality_trust import Action, Signer
from modality_trust.crypto import exact, identifier
from modality_trust.gateway import validate_challenge

from .trace import PROFILE, validate_pattern


def respond(signer: Signer, challenge: dict, action: Action, samples: list[list[int]], *, now: int) -> bytes:
    validate_challenge(challenge, now=now, modality="tactile")
    if challenge["request_digest"] != action.digest:
        raise ValueError("challenge is for another action")
    observation = {"profile": PROFILE, "resource": action.document["resource"], "samples": samples}
    appraise(observation, challenge, action.document)
    return signer.sign("tactile-evidence", {"challenge": challenge, "observation": observation})


def appraise(observation: dict, challenge: dict, action: dict) -> frozenset[str]:
    exact(observation, ("profile", "resource", "samples"))
    identifier(observation["resource"])
    if observation["profile"] != PROFILE or observation["resource"] != action["resource"]:
        raise ValueError("controller resource/profile mismatch")
    validate_pattern(observation["samples"], challenge)
    # Signed reports under a trusted sensor-path assumption, not a proof of toucher's identity.
    return frozenset({"reported-contact", "reported-pattern-match"})
