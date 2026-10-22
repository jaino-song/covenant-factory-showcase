# Evidence and limits

This showcase separates four evidence levels so readers can judge each claim at its actual scope. Architecture snapshot date: **2026-10-22**.

| Evidence level | What supports it | What it establishes |
|---|---|---|
| Source/design observations | Inspected current V2 methodology, runtime design, and QA candidate | The described role handoffs and candidate-bound evidence approach |
| Previously recorded local verification | Current inspected QA candidate’s recorded local implementation and regression status | Prior local verification was recorded; this showcase did not rerun those checks |
| Executed public reference | This repository’s Python evaluator, tests, and generated artifact | Deterministic behavior on the declared synthetic inputs |
| External integration | Actual Browserbase integration: NOT_RUN; cutover: BLOCKED in the recorded status | No live provider or cutover proof is offered here |

## What the broader project contributes

Factory V2 is an active cross-harness methodology/runtime, with documented separation among approved intent, independent PLAN review, scoped implementation, exact-candidate verification, independent CODE review, and Main-authorized QA where applicable. The current inspected QA candidate contains local implementation work; it should not be confused with a merged release or a deployed standalone Factory application.

The QA approach enumerates required evidence by case, assertion, viewport, and role, and checks candidate/build identity, producer, payload integrity, completeness, and observations. The public reference was authored afresh to make that principle inspectable. It includes no private source, original identifiers, histories, logs, internal links, or original test counts.

## What executes here

The demo constructs five synthetic submissions in memory. It evaluates strict record schemas, matching identity labels, manifest membership, duplicate exclusion, payload SHA-256, required coverage, and observation status. Its ten checks verify the five expected outcomes and preservation of their inputs. Unit tests independently exercise additional positive and negative paths and compare the generated artifact with current execution.

The artifact is a record of this reference program’s output. It is neither an authentic provider receipt nor a real Factory run. Its `provider_calls: 0` is consistent with a program containing no provider client, networking, subprocess, browser, model, environment access, or host-configuration writes.

## What the sample leaves open

- Real browser observations, accessibility/visual assertions, and the quality of the observations themselves.
- Authenticated producer provenance, trusted evidence transport, and binding real build artifacts to source.
- Main-only dispatch enforcement, read-only QA enforcement, bounded invocation/retest enforcement, and second-model inference controls.
- Multi-agent coordination, concurrency, durable storage/recovery, provider lifecycle management, deployment, and release authorization.

Those require their own implementations, trusted execution boundaries, and operational verification. An in-process fixture cannot establish them.

## How to read PASS

PASS means every one of four fictional required tuples has an eligible satisfied observation under this example’s rules. It does not prove the fixture told the truth, that all relevant product behaviors were specified, or that a real system is ready for release. Hashes can identify an accidental payload mismatch; they are not signatures or proof of an authentic provider.

The evaluator can refuse an invalid submission while retaining coverage gaps in its result. It can also report FAIL alongside missing or unknown requirements. This is why inspectable reasons and unmet checks matter: a single status label cannot explain the whole evidence state.

Human release decisions stay outside this evaluator. `release_authorized` remains false for every scenario and every verdict.
