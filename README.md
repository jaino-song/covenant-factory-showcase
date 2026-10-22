# Covenant Labs Factory — Evidence-driven agent workflows

An agent can finish a task and still leave a reviewer unable to answer three questions: **what changed, what was checked, and does that evidence belong to this candidate?** Covenant Labs Factory explores how to make those answers inspectable across design, implementation, review, and QA.

Factory V2 is an active engineering project built as a cross-harness methodology and runtime. Its workflow connects an approved mission and acceptance criteria to scoped worker contracts, independent reviews, candidate-bound verification, and human decisions. The interesting engineering problem is the handoff: keeping intent, implementation, evidence, and authority connected as work moves between roles.

This repository presents that architecture and a **newly authored public reference implementation using synthetic inputs**. The runnable slice demonstrates evidence reconciliation. It is separate from the private project’s source and does not claim implementation parity.

## The engineering approach

- **Define success before dispatch.** Acceptance criteria inform design, tests, and a worker’s bounded implementation contract.
- **Review at distinct stages.** Independent PLAN and CODE reviews serve different purposes; implementation success does not replace either review.
- **Bind checks to a candidate.** Candidate/build identity, evidence producer, payload integrity, and required coverage matter alongside observations.
- **Keep authority explicit.** Main authorizes applicable QA; humans retain mission approval and release decisions. A QA verdict is evidence for a decision.

For browser QA, required coverage can be enumerated as **case × assertion × viewport × role**. A successful run message cannot establish that every required combination was observed. The reference makes this distinction executable.

## Run it in 60 seconds

From this directory, with Python 3.10 or later:

```sh
python3 demo.py
python3 demo.py --json
python3 -m unittest discover -s tests -v
```

No installation or credentials are needed. The demo creates fictional evidence in memory, evaluates a frozen four-tuple manifest, and prints five honest outcomes:

| Scenario | Result | What it demonstrates |
|---|---|---|
| Complete evidence | PASS | Every required tuple has a matched, satisfied observation |
| Missing visual evidence | INCONCLUSIVE | An unobserved assertion cannot justify PASS |
| Stale candidate | REFUSED | Evidence from a different candidate is ineligible |
| Integrity mismatch | REFUSED | A changed payload fails its recorded digest |
| Seeded defect | FAIL | A valid observation reports a violated required assertion |

The final `Checks: 10/10 PASS` means the five expected verdicts and five input-preservation checks behaved correctly. It does **not** turn the incomplete, refused, or failed scenarios into successful QA. JSON always reports `synthetic: true`, `provider_calls: 0`, and `release_authorized: false`. Payload SHA-256 checks integrity; hashes do not authenticate a provider.

[The generated JSON artifact](artifacts/demo-output.json) is the deterministic result of actually running this public demo. No browser, model, agent, network, or provider integration executes here.

## Project context

Architecture snapshot: **2026-10-22**. The current inspected V2 QA candidate has previously recorded local implementation and regression verification. This repository does not rerun those private checks. Actual Browserbase integration remains **NOT_RUN**, and cutover remains **BLOCKED** in that recorded status. This is an architecture and reference snapshot, not a claim of a deployed standalone Factory application or a merged release.

## Explore the design

| Document | Focus |
|---|---|
| [Architecture](docs/architecture.md) | The V2 role flow, human authority, and the public reference boundary |
| [Design decisions](docs/design-decisions.md) | Frozen coverage, strict records, verdict precedence, and integrity limits |
| [Demo walkthrough](docs/demo-walkthrough.md) | The fixture, five scenarios, result schema, and verification commands |
| [Evidence and limits](docs/evidence-and-limits.md) | What is observed, previously recorded, executed here, and unrun |
