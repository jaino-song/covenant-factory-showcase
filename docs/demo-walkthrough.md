# Walkthrough: five evidence submissions

Run all commands from this directory with Python 3.10+. No packages need installation.

```sh
python3 demo.py
```

The walkthrough evaluates five submissions, explains each result, and ends with `Checks: 10/10 PASS`. That count consists of five expected-verdict checks and five input-preservation checks. The defect still has a FAIL verdict; the demo is successful because it detects that defect.

## 1. Freeze the fictional requirements

| Case | Assertion | Viewport | Role |
|---|---|---|---|
| summary-card | heading-visible | compact | reader |
| summary-card | heading-visible | wide | reader |
| detail-card | action-visible | compact | reader |
| detail-card | action-visible | wide | reader |

The expected labels are `synthetic-candidate-01`, `synthetic-build-01`, and producer `in-process-fixture`. They do not identify real source, a deployed build, or an authentic external producer.

## 2. Evaluate the submissions

**Complete → PASS.** Four fresh records carry satisfied observations, matching labels, and valid payload digests. No unmet checks remain.

**Missing visual → INCONCLUSIVE.** The wide detail-card record is omitted. Three validated records cannot prove the fourth required assertion; its tuple appears in `unmet_checks` with reason `missing`.

**Stale candidate → REFUSED.** One record labels an older synthetic candidate. The evaluator refuses the submission even though the supplied payloads say their assertions were satisfied.

**Integrity mismatch → REFUSED.** One detail payload changes after its digest was computed. Matching tuple and identity labels cannot compensate for that mismatch.

**Seeded defect → FAIL.** A correctly formed, correctly hashed observation reports that the compact detail-card action is absent. This is eligible evidence of a violated assertion, so it must fail.

## 3. Inspect the JSON

```sh
python3 demo.py --json
```

The CLI emits exactly one JSON object. Its top-level fields are:

| Field | Meaning |
|---|---|
| `demo` | Stable reference-demo name |
| `synthetic` | Always `true` |
| `provider_calls` | Always `0`; there is no provider execution code |
| `release_authorized` | Always `false` |
| `manifest`, `identity` | The frozen example coverage and fictional labels |
| `checks` | Ten `{id, passed, evidence}` reference-behavior checks |
| `scenarios` | Five bounded `{id, event, result}` records |

Each `result` contains `verdict`, concrete `reasons`, tuple-level `unmet_checks`, `required_records`, `validated_records`, and `release_authorized`. Validated records satisfy schema, membership, identity, uniqueness, and integrity checks; their observation can still be unknown or violated. Invalid records cannot satisfy coverage. No result authenticates provenance.

The CLI exits zero only if every reference check passes. Unsupported arguments exit with a usage error. There is no host-target option or external input loader.

## 4. Verify and reproduce

```sh
python3 -m unittest discover -s tests -v
python3 demo.py
python3 demo.py --json
python3 -m py_compile demo.py tests/test_demo.py
```

The unit suite exercises complete evidence, missing and unknown observations, empty and malformed inputs, all identity labels, strict schemas and identifiers, duplicate/extra tuples, integrity controls, precedence, input preservation, a frozen manifest, CLI behavior, and artifact equality. These are tests of this public implementation, not private Factory regression results.

To regenerate the checked-in artifact from actual execution:

```sh
python3 demo.py --json > artifacts/demo-output.json
```

The result is stable across runs: no timestamps, random values, host paths, browser sessions, or provider responses are involved. Normal demo execution writes nothing. The verification commands may create ignored Python bytecode caches; the artifact redirection explicitly writes the named project artifact.
