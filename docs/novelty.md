# Research position and prior art

Haptic and touch-based authentication already include behavioral biometrics,
passcodes and challenge-response interaction. OpenATT is not a biometric matcher
or an identification system. Its eight-bit pattern does not claim anti-relay
security. WebAuthn distinguishes user presence, user verification and relying-party
verification; arbitrary controller contact does not inherit those ceremonies.

RATS separates reported evidence from appraisal and relying-party authorization.
Sensor-injection research such as WALNUT illustrates why signed digital output
cannot establish trustworthy analog sensing. CaMeL and Fides supply policy/IFC
precedents; OpenATT does not reimplement their planners or compare to their
published agent results. Hysteresis, signed reports and database transactions
are established techniques, not research novelty.

The contribution currently supported is an inspectable implementation and local
negative-result suite exposing contact/consent, capture freshness and short-pattern
limitations. Broader novelty in composition and selective evidence acquisition
requires formalization and evaluation against equally expressive controls.

Primary sources checked October 31, 2026:

- [WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/)
- [Haptic-Based User Authentication for Tele-robotic System](https://arxiv.org/abs/2506.14116)
- [TouchIn](https://arxiv.org/abs/1402.1216)
- [WALNUT](https://spqrlab1.github.io/papers/trippel-IEEE-oaklawn-walnut-2017.pdf)
- [RATS architecture](https://www.rfc-editor.org/rfc/rfc9334.html)
- [CaMeL](https://arxiv.org/abs/2503.18813)
- [Fides](https://arxiv.org/abs/2505.23643)
