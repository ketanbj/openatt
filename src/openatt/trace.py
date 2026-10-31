"""Bounded force/time input, hysteretic segmentation and a nonce-dependent pattern.

Units are integer milliseconds and millinewtons. Thresholds are a versioned
fixture profile, not calibrated measurements or a universal tactile classifier.
"""

import csv
import hashlib
import random
from pathlib import Path

from modality_trust import canonical
from modality_trust.crypto import integer

MAX_SAMPLES = 512
MAX_DURATION_MS = 5000
PROFILE = "contact-pattern-v1"


def pattern(challenge: dict) -> list[int]:
    """Eight short/long contacts (8 bits), for binding checks, never distance bounding."""
    byte = hashlib.sha256(canonical(challenge)).digest()[0]
    return [100 if (byte >> bit) & 1 == 0 else 200 for bit in range(8)]


def analyze(samples: list[list[int]]) -> list[list[int]]:
    if type(samples) is not list or not 10 <= len(samples) <= MAX_SAMPLES:
        raise ValueError("sample count out of profile")
    previous, contact_start, contacts = None, None, []
    for sample in samples:
        if type(sample) is not list or len(sample) != 2:
            raise ValueError("sample must be [milliseconds, millinewtons]")
        timestamp, force = integer(sample[0], 0, MAX_DURATION_MS), integer(sample[1], 0, 20000)
        if previous is None and timestamp != 0:
            raise ValueError("trace must begin at zero")
        if previous is not None and not 1 <= timestamp - previous <= 20:
            raise ValueError("nonmonotonic samples or acquisition gap")
        if contact_start is None and force >= 500:
            contact_start = timestamp
        elif contact_start is not None and force <= 200:
            if timestamp - contact_start < 40:
                raise ValueError("contact shorter than debounce interval")
            contacts.append([contact_start, timestamp - contact_start])
            contact_start = None
        previous = timestamp
    if contact_start is not None:
        raise ValueError("trace ends during contact")
    return contacts


def validate_pattern(samples: list[list[int]], challenge: dict) -> list[list[int]]:
    contacts = analyze(samples)
    expected = pattern(challenge)
    if len(contacts) != len(expected):
        raise ValueError("wrong contact count")
    for index, ((start, duration), target) in enumerate(zip(contacts, expected)):
        if abs(duration - target) > 20:
            raise ValueError("challenge pattern mismatch")
        if index == 0:
            gap = start
        else:
            old_start, old_duration = contacts[index - 1]
            gap = start - old_start - old_duration
        if not 80 <= gap <= 120:
            raise ValueError("contact spacing mismatch")
    return contacts


def simulate(challenge: dict, *, seed=0, noise_mn=0, jitter_ms=0) -> list[list[int]]:
    """Generated fixture data, never represented as hardware acquisition."""
    if type(noise_mn) is not int or not 0 <= noise_mn <= 1500:
        raise ValueError("noise out of simulator range")
    if type(jitter_ms) is not int or not 0 <= jitter_ms <= 50:
        raise ValueError("jitter out of simulator range")
    rng, intervals, cursor = random.Random(seed), [], 100
    for duration in pattern(challenge):
        duration += rng.randint(-jitter_ms, jitter_ms)
        intervals.append((cursor, cursor + duration))
        cursor += duration + 100
    result = []
    for timestamp in range(0, cursor + 1, 10):
        active = any(start <= timestamp < end for start, end in intervals)
        base = 1000 if active else 0
        result.append([timestamp, max(0, base + rng.randint(-noise_mn, noise_mn))])
    return result


def read_csv(path: str | Path) -> list[list[int]]:
    """File boundary for a trusted acquisition process; CSV itself is unauthenticated."""
    path = Path(path)
    if path.stat().st_size > 65536:
        raise ValueError("CSV byte limit")
    with path.open(newline="") as stream:
        reader = csv.reader(stream)
        if next(reader, None) != ["time_ms", "force_mn"]:
            raise ValueError("expected time_ms,force_mn header")
        samples = []
        for row in reader:
            if len(samples) >= MAX_SAMPLES or len(row) != 2:
                raise ValueError("CSV sample limit or shape")
            try:
                samples.append([int(row[0]), int(row[1])])
            except ValueError as error:
                raise ValueError("CSV must contain integer units") from error
    analyze(samples)
    return samples


def write_csv(path: str | Path, samples: list[list[int]]):
    analyze(samples)
    with Path(path).open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_ms", "force_mn"])
        writer.writerows(samples)
