# OpenATT threat model

The adversary can replay or edit traces, omit samples, alter timestamps or force,
substitute actions/resources, relay controller messages, invoke duplicate actions,
and race revocation. The verifier, clock, controller/owner keys and sensor-to-signing
path are trusted. No hardware root of trust or calibrated sensor is implemented.

- Trace shape, nonmonotonic time, acquisition gaps and malformed contacts fail closed.
- Changed challenge/session/action fields or tampered signed samples are denied.
- Grants supply permission separately from contact. Requiring human consent,
  physical proximity or toucher identity is unsupported and must be denied.
- A configured malicious controller can synthesize an apparently valid trace for
  any challenge. Pattern matching cannot detect that compromise.
- An old trace has a 1/256 random chance of matching an unrelated 8-bit pattern.
  The benchmark records actual collisions. The pattern alone is not authentication.
- Even honest pattern matching measures reported contact under capture assumptions;
  it does not prove intent, willingness, biological identity or safe actuation.
- Native device drivers, secure enrollment, anti-tamper hardware, calibration,
  actuator safety and user-consent ceremonies remain outside the implementation.

All released signal trials use generated traces. No real user, sensor, robot,
physical relay or haptic actuator was evaluated. Processing cost excludes the
simulated physical contact duration. A local receipt is the sole durable effect.
