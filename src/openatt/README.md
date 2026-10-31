# Implementation map

- `trace.py`: bounded CSV input, integer units, hysteretic segmentation,
  challenge-derived short/long pattern and explicitly generated trace fixtures.
- `protocol.py`: signed controller reports and independent trace appraisal.
- `cli.py`: local demonstration and unauthenticated CSV inspection.
- `modality_trust` (umbrella `core/`): permission and transactional local receipts.

A controller signature authenticates report bytes. It does not establish sensor
truth, toucher identity, intent, consent, proximity or safe actuation.
