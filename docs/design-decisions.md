# Design decisions

## Coverage is a contract

A runner can report success after observing only part of a journey. A separate required manifest lets a consumer ask which assertions have evidence rather than relying on a producer’s summary.

The toy manifest enumerates exactly four tuples: two fictional card cases, each in `compact` and `wide` viewports, for the `reader` role. Each case has one required visual assertion. It is a bounded example, not exhaustive product coverage or the full Cartesian product of every label.

The manifest is a tuple of frozen dataclasses. Callers supply evidence only; they cannot use the evaluator API to substitute weaker coverage requirements.

## Evidence must be eligible before it is persuasive

Each record has exactly nine fields: `case`, `assertion`, `viewport`, `role`, `candidate`, `build`, `producer`, `payload`, and `payload_sha256`. Identifiers use a strict lowercase ASCII slug format, and the four-tuple must appear in the manifest. Candidate, build, and producer must match the fixed synthetic contract.

The payload has exactly `observation` and `detail`. The observation is `satisfied`, `violated`, or `unknown`; detail is nonblank text of at most 240 characters. Missing fields, extra fields, wrong types, malformed identifiers, extra tuples, duplicate tuples, unexpected identity labels, and invalid integrity all produce `REFUSED`.

Duplicates are refused even when their observations agree. Allowing the last record to win could hide an earlier defect; allowing the first to win could hide a later defect. This example refuses ambiguity instead of choosing an observation.

## Verdict precedence is explicit

| Priority | Condition | Verdict |
|---|---|---|
| 1 | Any supplied record is ineligible or malformed | REFUSED |
| 2 | Otherwise, any required assertion is observed violated | FAIL |
| 3 | Otherwise, any required tuple is absent or its observation is unknown | INCONCLUSIVE |
| 4 | Otherwise, every required assertion is observed satisfied | PASS |

An empty list is well-formed incomplete evidence and returns `INCONCLUSIVE`. A non-list input is malformed and returns `REFUSED`. A valid violation with missing evidence returns `FAIL`. A valid violation plus any malformed record returns `REFUSED`. Every result retains unmet requirements, so the primary verdict does not erase other gaps.

These are declared rules for this public reference. They illustrate the grounded principle that missing, unknown, or ambiguous evidence cannot justify PASS; they do not define or alter private Factory policy or claim matching internal schemas.

## Integrity is narrower than authenticity

The payload digest is SHA-256 of UTF-8 JSON with sorted keys, compact separators, and ASCII escaping. It catches payload edits that do not update the recorded digest. Anyone able to replace both payload and digest can generate a matching pair; identity and producer values here are labels, not authenticated provenance.

The tests include that positive control deliberately: an edited payload with a recomputed digest remains eligible if its schema and labels match. Authentic provider provenance would require an independently trusted mechanism outside this sample. The demo makes no such claim.

## Evaluation preserves state

The evaluator reads plain data and returns a fresh result. Refused and incomplete evidence stay unchanged, allowing inspection of the original submission. Since no external action or state mutation occurs, this slice needs no transaction rollback. Immutability checks cover the manifest and caller evidence across positive and negative paths.

## Evidence does not carry release authority

Every result includes `release_authorized: false`, including PASS. The public reference contains no release action. In the larger design, authorization is a separate human decision informed by implementation, review, QA, and other applicable evidence.
