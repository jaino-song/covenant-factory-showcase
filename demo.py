"""Synthetic evidence reconciliation. Python 3.10+, standard library only."""

import argparse
from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import re


@dataclass(frozen=True)
class Requirement:
    case: str
    assertion: str
    viewport: str
    role: str


# An enumerated toy contract, not a Cartesian-product coverage claim.
MANIFEST = (
    Requirement("summary-card", "heading-visible", "compact", "reader"),
    Requirement("summary-card", "heading-visible", "wide", "reader"),
    Requirement("detail-card", "action-visible", "compact", "reader"),
    Requirement("detail-card", "action-visible", "wide", "reader"),
)
CANDIDATE = "synthetic-candidate-01"
BUILD = "synthetic-build-01"
PRODUCER = "in-process-fixture"
IDENTIFIER = re.compile(r"[a-z][a-z0-9-]{0,47}", re.ASCII)
DIGEST = re.compile(r"[0-9a-f]{64}", re.ASCII)
TUPLE_FIELDS = ("case", "assertion", "viewport", "role")
IDENTITY = {"candidate": CANDIDATE, "build": BUILD, "producer": PRODUCER}
RECORD_FIELDS = frozenset((*TUPLE_FIELDS, *IDENTITY, "payload", "payload_sha256"))
OBSERVATIONS = frozenset(("satisfied", "violated", "unknown"))
MAX_DETAIL_LENGTH = 240


def payload_digest(payload: dict) -> str:
    """Hash canonical JSON bytes; this is integrity, never authentication."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def make_evidence() -> list[dict]:
    """Create fresh fictional observations without invoking a browser or agent."""
    records = []
    for requirement in MANIFEST:
        payload = {"observation": "satisfied", "detail": "Synthetic assertion satisfied."}
        records.append({**asdict(requirement), **IDENTITY, "payload": payload,
                        "payload_sha256": payload_digest(payload)})
    return records


def evaluate(evidence: object) -> dict:
    """Reconcile plain Python data against the frozen example contract, read-only.

    Precedence: REFUSED > FAIL > INCONCLUSIVE > PASS. Validate every supplied
    record before trusting observations. No caller data is repaired or changed.
    """
    refusals = []
    observations = {}
    seen = set()
    records = evidence if type(evidence) is list else []
    if type(evidence) is not list:
        refusals.append("Evidence must be a list of records.")

    for index, record in enumerate(records):
        prefix = f"Record {index + 1}"
        if type(record) is not dict or record.keys() != RECORD_FIELDS:
            refusals.append(f"{prefix}: expected the exact record fields.")
            continue
        identifiers = (*TUPLE_FIELDS, *IDENTITY)
        if any(type(record[field]) is not str or
               IDENTIFIER.fullmatch(record[field]) is None for field in identifiers):
            refusals.append(f"{prefix}: malformed tuple or identity identifier.")
            continue
        requirement = Requirement(*(record[field] for field in TUPLE_FIELDS))
        if requirement not in MANIFEST:
            refusals.append(f"{prefix}: tuple is outside the required manifest.")
            continue
        if requirement in seen:
            refusals.append(f"{prefix}: duplicate tuple cannot shadow an observation.")
            continue
        seen.add(requirement)
        if any(record[field] != expected for field, expected in IDENTITY.items()):
            refusals.append(f"{prefix}: candidate, build or producer does not match.")
            continue
        payload = record["payload"]
        if (type(payload) is not dict or payload.keys() != {"observation", "detail"}
                or type(payload["observation"]) is not str
                or payload["observation"] not in OBSERVATIONS
                or type(payload["detail"]) is not str
                or not payload["detail"].strip()
                or len(payload["detail"]) > MAX_DETAIL_LENGTH):
            refusals.append(f"{prefix}: malformed observation payload.")
            continue
        digest = record["payload_sha256"]
        if (type(digest) is not str or DIGEST.fullmatch(digest) is None
                or digest != payload_digest(payload)):
            refusals.append(f"{prefix}: payload integrity check did not match.")
            continue
        observations[requirement] = payload["observation"]

    unmet = []
    for requirement in MANIFEST:
        observation = observations.get(requirement)
        if observation != "satisfied":
            unmet.append({**asdict(requirement), "reason": observation or "missing"})
    if refusals:
        verdict, reasons = "REFUSED", refusals
    elif "violated" in observations.values():
        verdict, reasons = "FAIL", ["A required assertion was observed violated."]
    elif unmet:
        verdict, reasons = "INCONCLUSIVE", ["Required evidence is missing or unknown."]
    else:
        verdict, reasons = "PASS", ["All four required tuples match and are satisfied."]
    return {"verdict": verdict, "reasons": reasons, "unmet_checks": unmet,
            "required_records": len(MANIFEST), "validated_records": len(observations),
            "release_authorized": False}


def run_demo() -> dict:
    complete = make_evidence()
    missing = deepcopy(complete[:-1])
    stale = deepcopy(complete)
    stale[0]["candidate"] = "synthetic-candidate-old"
    tampered = deepcopy(complete)
    tampered[0]["payload"]["detail"] = "Synthetic payload edited after hashing."
    defect = deepcopy(complete)
    defect[2]["payload"] = {"observation": "violated", "detail": "Synthetic action absent."}
    defect[2]["payload_sha256"] = payload_digest(defect[2]["payload"])
    examples = (
        ("complete", "Four matched synthetic observations supplied.", complete, "PASS"),
        ("missing-visual", "One visual observation deliberately omitted.", missing, "INCONCLUSIVE"),
        ("stale-candidate", "A record labels a different synthetic candidate.", stale, "REFUSED"),
        ("integrity-mismatch", "A payload changed without updating its digest.", tampered, "REFUSED"),
        ("seeded-defect", "A valid observation records an absent action.", defect, "FAIL"),
    )
    checks, scenarios = [], []
    for scenario_id, event, records, expected in examples:
        before = deepcopy(records)
        result = evaluate(records)
        checks.append({"id": scenario_id, "passed": result["verdict"] == expected,
                       "evidence": {"expected": expected, "observed": result["verdict"]}})
        checks.append({"id": f"{scenario_id}-input-preserved", "passed": before == records,
                       "evidence": "Input records equal their pre-evaluation snapshot."})
        scenarios.append({"id": scenario_id, "event": event, "result": result})
    return {"demo": "covenant-factory-evidence-reference", "synthetic": True,
            "provider_calls": 0, "release_authorized": False,
            "manifest": [asdict(item) for item in MANIFEST],
            "identity": dict(IDENTITY), "checks": checks, "scenarios": scenarios}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print deterministic synthetic results")
    args = parser.parse_args()
    output = run_demo()
    passed = all(check["passed"] for check in output["checks"])
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print("Covenant Labs Factory | evidence reference demo")
        print("Synthetic in-process inputs; no browser, agent or provider calls.\n")
        for scenario in output["scenarios"]:
            result = scenario["result"]
            print(f"{scenario['id']}: {result['verdict']} — {scenario['event']}")
            for reason in result["reasons"]:
                print(f"  {reason}")
        print(f"\nChecks: {sum(c['passed'] for c in output['checks'])}/{len(output['checks'])} "
              f"{'PASS' if passed else 'FAIL'}")
        print("Provider calls: 0 | Release authorized: false")
        print("Hashes check payload integrity; they do not authenticate a provider.")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
