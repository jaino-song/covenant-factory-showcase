# Covenant Labs Factory

**Multi-agent orchestration with reviewable work and verifiable completion.**

I’m building Factory to turn a software request into scoped agent work, independent reviews, and QA evidence tied to the code being assessed.

The problem is knowing when the work is actually done. An agent can report success while required checks are missing, failures remain unresolved, or the evidence belongs to an older revision. Factory’s design makes requirements, responsibilities, and verification explicit at each handoff.

The public demo makes one part of that design executable: **accept complete evidence, expose missing checks, and refuse evidence from the wrong candidate or build**.

**In development · Private implementation · Public architecture and synthetic reference demo.**

## What I’m building

- **Clear work packages:** requirements, acceptance criteria, tests, and implementation scope travel together when work moves between agents.
- **Separate design and code reviews:** a design review checks the proposed approach; a code review examines the resulting change and its verification.
- **Evidence tied to the work:** checks identify the candidate, build, producer, and required observations so a result from another revision cannot stand in for current evidence.
- **Explicit decision ownership:** Main authorizes applicable QA; humans retain mission approval and release decisions. A passing QA result does not grant release authority.

For browser QA, required coverage can be listed as **case × assertion × viewport × role**. The reference demo checks that coverage directly, showing why a success message alone is not enough.

The demo is separately authored, uses synthetic inputs, and covers only this evidence-checking slice. It does not execute the private multi-agent workflow or claim implementation parity.

## Run the evidence-checking demo

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

## Current project status

Documentation refreshed **2026-10-27**, using the latest inspected QA record dated **2026-10-24**.

| Area | Verified scope |
|---|---|
| Public reference | Runnable synthetic evaluator, unit tests, and deterministic output in this repository |
| Private project record | Prior local implementation and regression checks are recorded; they were not rerun for this showcase |
| Cloud-browser smoke | An operator captured and reviewed four public landing/sign-in views across desktop, tablet, and mobile sizes |
| Product QA | Inconclusive: authenticated workflows, persistence, and formal agent-driven QA remain unverified |

The browser smoke establishes only those public-screen observations. The private main branch has advanced beyond the recorded QA candidate, so these results do not verify its latest state. Production merge, deployment, and cutover are not established by this evidence. See [evidence and limits](docs/evidence-and-limits.md) for the full boundary.

## Explore the design

| Document | Focus |
|---|---|
| [Architecture](docs/architecture.md) | The V2 role flow, human authority, and the public reference boundary |
| [Design decisions](docs/design-decisions.md) | Frozen coverage, strict records, verdict precedence, and integrity limits |
| [Demo walkthrough](docs/demo-walkthrough.md) | The fixture, five scenarios, result schema, and verification commands |
| [Evidence and limits](docs/evidence-and-limits.md) | What is observed, previously recorded, executed here, and unrun |
