# OpenATT architecture

A fixture assistant observes contact with a release surface. The controller may
report a matching challenge pattern, but this does not authorize a release and
cannot identify a consenting human. OpenATT keeps the contact report and action
permission separate.

`Action -> stored challenge -> short/long contact pattern -> bounded force trace
-> controller signature -> independent signal appraisal + grant -> local receipt`

The fixed fixture profile uses integer milliseconds/millinewtons, force-on 500 mN,
force-off 200 mN, minimum 40 ms contacts, monotonically increasing samples with a
maximum 20 ms gap, and at most 512 samples/5 seconds. A challenge hash selects eight
100/200 ms contacts separated by 100 ms; duration tolerance is 20 ms and spacing
is 80-120 ms. These are explicit engineering settings, not calibrated thresholds.

The CSV boundary accepts time_ms,force_mn records from an acquisition process.
CSV is unauthenticated. The trusted controller must ensure its capture really
occurred after the challenge; signing arbitrary input files does not establish
that. `respond` checks shape and pattern before signing, and the gateway repeats
the check. Released CSV fixtures are generated simulations, not sensor recordings.

Eight short/long contacts have only 256 patterns. They are acquisition consistency
checks, not secrets or cryptographic nonces. Old traces can match new patterns;
full signed random nonce/session binding provides message freshness under the
trusted controller assumption. Neither a pattern nor a signature proves proximity,
a new physical contact, truthful force measurements or human consent.

## Enforcement and trust

The verifier and gateway clock are trusted. Public keys are pinned out of band;
the demo generates them locally. Separate attester and owner trust maps prevent
an observation key from acting as the permission signer. A grant binds an exact
immutable principal/action/resource/purpose/arguments digest and business audience.
Nonce/session scope prevents reusing an old signed response for a new interaction.
A configured signer can lie; key possession is not identity proofing.

The SQLite write lock is the reference linearization boundary. Current grant and
issuer revocation, expiry, challenge/grant consumption and local receipt insertion
are checked in one transaction. After restart, consumed state remains unavailable.
No remote callback, payment, lock or robot movement is included in that guarantee.
Replay-state cleanup, account enrollment, clock synchronization and deployment
hardening remain work for production integration.

## Encoding

The shared local signing profile uses sorted ASCII-escaped JSON and a domain
separator, Ed25519, explicit version/kind/issuer fields, 32 KiB message bounds,
depth/collection limits and duplicate-key rejection. Floats, nonfinite values,
unknown fields and boolean timestamps are rejected. Signatures authenticate
structured bytes only. This profile is not JOSE, COSE, RFC 8785, or the draft
umbrella evidence schema. No wire interoperability is asserted.
