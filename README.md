# Covenant Labs Factory

**Multi-agent software development with a checkable definition of done.**

I’m building Factory to coordinate AI agents across **planning, implementation, independent review, and QA**.

The problem: an agent can report success while required checks are missing, failures remain unresolved, or the evidence comes from a different code revision. Coordinating the agents also means defining what work is required and how someone else can verify it.

My V2 design connects task requirements, scoped implementation, separate design and code reviews, and QA evidence tied to the code being assessed. The public example makes one part executable: checking whether submitted evidence covers the required assertions and belongs to the right candidate and build.

**In development · Private implementation · Public architecture and synthetic reference demo.**

## What I’m building

- **Clear work packages:** requirements, acceptance criteria, tests, and implementation scope travel together when work moves between agents.
- **Separate design and code reviews:** a design review checks the proposed approach; a code review examines the resulting change and its verification.
- **Evidence tied to the work:** checks identify the candidate, build, producer, and required observations so a result from another revision cannot stand in for current evidence.
- **Explicit decision ownership:** Main authorizes applicable QA; humans retain mission approval and release decisions. A passing QA result does not grant release authority.

For browser QA, required coverage can be listed as **case × assertion × viewport × role**. The reference demo checks that coverage directly, showing why a success message alone is not enough.

The demo is separately authored, uses synthetic inputs, and covers only this evidence-checking slice. It does not execute the private multi-agent workflow or claim implementation parity.

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
