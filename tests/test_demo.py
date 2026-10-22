"""Tests of this public reference, not of the private Factory implementation."""

from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import FrozenInstanceError
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import demo


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.records = demo.make_evidence()

    def assert_verdict(self, records, verdict):
        before = deepcopy(records)
        manifest_before = tuple(demo.MANIFEST)
        result = demo.evaluate(records)
        self.assertEqual(result["verdict"], verdict)
        self.assertIs(result["release_authorized"], False)
        self.assertEqual(records, before)
        self.assertEqual(demo.MANIFEST, manifest_before)
        return result

    def observe(self, index, observation):
        self.records[index]["payload"]["observation"] = observation
        self.records[index]["payload_sha256"] = demo.payload_digest(self.records[index]["payload"])

    def test_complete_positive_control(self):
        result = self.assert_verdict(self.records, "PASS")
        self.assertEqual(result["validated_records"], 4)
        self.assertEqual(result["unmet_checks"], [])

    def test_order_does_not_change_coverage(self):
        self.assertEqual(demo.evaluate(self.records), demo.evaluate(list(reversed(self.records))))

    def test_missing_required_visual_tuple(self):
        removed = self.records.pop()
        result = self.assert_verdict(self.records, "INCONCLUSIVE")
        self.assertEqual(result["unmet_checks"], [
            {field: removed[field] for field in demo.TUPLE_FIELDS} | {"reason": "missing"}
        ])

    def test_empty_list_has_all_four_unmet_requirements(self):
        result = self.assert_verdict([], "INCONCLUSIVE")
        self.assertEqual(len(result["unmet_checks"]), 4)
        self.assertEqual(result["validated_records"], 0)

    def test_unknown_observation_is_inconclusive(self):
        self.observe(0, "unknown")
        result = self.assert_verdict(self.records, "INCONCLUSIVE")
        self.assertEqual(result["unmet_checks"][0]["reason"], "unknown")

    def test_observed_defect_fails(self):
        self.observe(1, "violated")
        result = self.assert_verdict(self.records, "FAIL")
        self.assertEqual(result["unmet_checks"][0]["reason"], "violated")

    def test_fail_precedes_missing_and_unknown(self):
        self.observe(0, "violated")
        self.observe(1, "unknown")
        self.records.pop()
        result = self.assert_verdict(self.records, "FAIL")
        self.assertEqual({item["reason"] for item in result["unmet_checks"]},
                         {"violated", "unknown", "missing"})

    def test_each_identity_label_must_match(self):
        for field in demo.IDENTITY:
            with self.subTest(field=field):
                records = deepcopy(self.records)
                records[0][field] = "different-fixture"
                self.assert_verdict(records, "REFUSED")

    def test_tamper_refused_and_rehashed_positive_control(self):
        self.records[0]["payload"]["detail"] = "Another synthetic observation detail."
        self.assert_verdict(self.records, "REFUSED")
        self.records[0]["payload_sha256"] = demo.payload_digest(self.records[0]["payload"])
        self.assert_verdict(self.records, "PASS")  # Hashes are not authentication.

    def test_invalid_digests_refused(self):
        for digest in (None, 17, "", "f" * 63, "F" * 64, "g" * 64, "0" * 64):
            with self.subTest(digest=digest):
                records = deepcopy(self.records)
                records[0]["payload_sha256"] = digest
                self.assert_verdict(records, "REFUSED")

    def test_duplicates_never_shadow_a_violation(self):
        violated = deepcopy(self.records[0])
        violated["payload"]["observation"] = "violated"
        violated["payload_sha256"] = demo.payload_digest(violated["payload"])
        for records in (self.records + [violated], [violated] + self.records):
            self.assert_verdict(records, "REFUSED")

    def test_extra_tuple_refused(self):
        for field in demo.TUPLE_FIELDS:
            with self.subTest(field=field):
                records = deepcopy(self.records)
                records[0][field] = "unrequired-value"
                self.assert_verdict(records, "REFUSED")

    def test_strict_identifier_shapes(self):
        invalid = (None, False, 1, [], {}, "", "Wide", "wide\n", "../wide", "é", "a" * 49)
        for field in (*demo.TUPLE_FIELDS, *demo.IDENTITY):
            for value in invalid:
                with self.subTest(field=field, value=value):
                    records = deepcopy(self.records)
                    records[0][field] = value
                    self.assert_verdict(records, "REFUSED")

    def test_non_list_and_malformed_records(self):
        for value in (None, {}, "", (), False, [None], [3], [[]], ["record"]):
            with self.subTest(value=value):
                self.assert_verdict(value, "REFUSED")

    def test_each_record_field_is_required(self):
        for field in demo.RECORD_FIELDS:
            with self.subTest(field=field):
                records = deepcopy(self.records)
                del records[0][field]
                self.assert_verdict(records, "REFUSED")

    def test_extra_record_field_refused(self):
        self.records[0]["unexpected"] = True
        self.assert_verdict(self.records, "REFUSED")

    def test_payload_schema_is_strict(self):
        invalid = (None, [], {}, {"observation": "satisfied"},
                   {"observation": "satisfied", "detail": "ok", "extra": True},
                   {"observation": "success", "detail": "ok"},
                   {"observation": True, "detail": "ok"},
                   {"observation": [], "detail": "ok"},
                   {"observation": "satisfied", "detail": None},
                   {"observation": "satisfied", "detail": "  "},
                   {"observation": "satisfied", "detail": "x" * 241})
        for payload in invalid:
            with self.subTest(payload=payload):
                records = deepcopy(self.records)
                records[0]["payload"] = payload
                self.assert_verdict(records, "REFUSED")

    def test_refused_precedes_fail_and_inconclusive(self):
        self.observe(0, "violated")
        self.observe(1, "unknown")
        self.records[2]["build"] = "different-build"
        self.records.pop()
        self.assert_verdict(self.records, "REFUSED")

    def test_later_invalid_record_cannot_be_hidden_by_early_failure(self):
        self.observe(0, "violated")
        self.records.append({})
        self.assert_verdict(self.records, "REFUSED")

    def test_manifest_is_frozen(self):
        self.assertIsInstance(demo.MANIFEST, tuple)
        self.assertEqual(len(set(demo.MANIFEST)), 4)
        with self.assertRaises(FrozenInstanceError):
            demo.MANIFEST[0].case = "changed"

    def test_fresh_fixture_does_not_share_mutable_payloads(self):
        self.records[0]["payload"]["detail"] = "Modified fixture."
        self.assert_verdict(demo.make_evidence(), "PASS")
        self.assertNotEqual(self.records[0]["payload"], self.records[1]["payload"])

    def test_digest_uses_canonical_json(self):
        first = {"detail": "Synthetic café.", "observation": "satisfied"}
        second = {"observation": "satisfied", "detail": "Synthetic café."}
        self.assertEqual(demo.payload_digest(first), demo.payload_digest(second))
        second["observation"] = "unknown"
        self.assertNotEqual(demo.payload_digest(first), demo.payload_digest(second))


class DemonstrationTests(unittest.TestCase):
    def test_scenarios_keep_honest_verdicts_and_never_authorize_release(self):
        output = demo.run_demo()
        self.assertIs(output["synthetic"], True)
        self.assertEqual(output["provider_calls"], 0)
        self.assertIs(output["release_authorized"], False)
        self.assertEqual([item["result"]["verdict"] for item in output["scenarios"]],
                         ["PASS", "INCONCLUSIVE", "REFUSED", "REFUSED", "FAIL"])
        self.assertEqual(len(output["checks"]), 10)
        self.assertTrue(all(check["passed"] for check in output["checks"]))

    def test_demo_and_checked_in_artifact_are_deterministic(self):
        artifact = Path(__file__).resolve().parents[1] / "artifacts" / "demo-output.json"
        self.assertEqual(demo.run_demo(), demo.run_demo())
        self.assertEqual(json.loads(artifact.read_text(encoding="utf-8")), demo.run_demo())

    def test_json_cli_emits_one_object(self):
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["demo.py", "--json"]), redirect_stdout(stdout):
            self.assertEqual(demo.main(), 0)
        self.assertEqual(json.loads(stdout.getvalue()), demo.run_demo())

    def test_walkthrough_explains_result_and_scope(self):
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["demo.py"]), redirect_stdout(stdout):
            self.assertEqual(demo.main(), 0)
        self.assertIn("Checks: 10/10 PASS", stdout.getvalue())
        self.assertIn("Release authorized: false", stdout.getvalue())

    def test_failed_reference_check_gives_nonzero_exit(self):
        output = demo.run_demo()
        output["checks"][0]["passed"] = False
        with patch.object(demo, "run_demo", return_value=output), \
                patch.object(sys, "argv", ["demo.py", "--json"]), redirect_stdout(io.StringIO()):
            self.assertEqual(demo.main(), 1)

    def test_cli_has_no_host_target_option(self):
        with patch.object(sys, "argv", ["demo.py", "--target", "fictional"]), \
                redirect_stdout(io.StringIO()), unittest.mock.patch("sys.stderr", new=io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                demo.main()
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
