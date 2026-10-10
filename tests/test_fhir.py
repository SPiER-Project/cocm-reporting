"""Tests for reading FHIR resources into the data-contract tables.

    python3 -m unittest discover tests

The screening example as a FHIR Bundle (tests/fixtures/screening-example-fhir) is checked
against its expected results by test_calculator.py. These tests check the mapping rules.
"""

import csv
import io
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from calculator import read_rules  # noqa: E402
from calculator.data import combine  # noqa: E402
from calculator.fhir import read_fhir  # noqa: E402

with open(os.path.join(ROOT, "rules", "calls.toml")) as f:
    SETTINGS = read_rules(f.read())
SOPT = "https://nahdo.org/sopt"


def rows(text):
    return list(csv.DictReader(io.StringIO(text)))


def bundle(*resources):
    return json.dumps({"resourceType": "Bundle", "type": "collection",
                       "entry": [{"resource": r} for r in resources]})


def coverage(code=None, plan=None, pid="X"):
    r = {"resourceType": "Coverage", "id": f"cov-{code}-{plan}", "status": "active",
         "beneficiary": {"reference": f"Patient/{pid}"}, "period": {"start": "2024-01-01"}}
    if code:
        r["type"] = {"coding": [{"system": SOPT, "code": code}]}
    if plan:
        r["class"] = [{"type": {"coding": [{"code": "plan"}]}, "value": "p", "name": plan}]
    return r


PATIENT = {"resourceType": "Patient", "id": "X", "birthDate": "1980-01-01",
           "identifier": [{"system": "urn:site:registry", "value": "R-42"}]}


class CoverageTests(unittest.TestCase):
    def category(self, **kw):
        tables, notes = read_fhir([bundle(PATIENT, coverage(**kw))], SETTINGS)
        return rows(tables["coverage"])[0]["payer_category"], notes

    def test_payer_type_codes(self):
        cases = {
            "21": "medicaid_managed_care", "211": "medicaid_managed_care",
            "22": "medicaid_ffs", "2": "medicaid_ffs",
            "14": "dual_medicare_medicaid", "141": "dual_medicare_medicaid",
            "121": "medicare", "23": "child_health_plus",
            "25": "other",  # out-of-state Medicaid isn't New York State Medicaid
            "511": "commercial", "611": "commercial", "81": "self_pay", "95": "other",
        }
        for code, want in cases.items():
            with self.subTest(code=code):
                self.assertEqual(self.category(code=code)[0], want)

    def test_new_york_programs_by_plan_name(self):
        self.assertEqual(self.category(code="36", plan="Plan Q Essential Plan")[0], "essential_plan")
        self.assertEqual(self.category(code="23", plan="Child Health Plus")[0], "child_health_plus")

    def test_unrecognized_coverage_is_other_with_a_note(self):
        category, notes = self.category(plan="Mystery Plan")
        self.assertEqual(category, "other")
        self.assertTrue(any("Mystery Plan" in n for n in notes))


class PatientTests(unittest.TestCase):
    def test_patient_id_from_an_identifier_system(self):
        obs = {"resourceType": "Observation", "id": "o", "status": "final",
               "code": {"coding": [{"system": "http://loinc.org", "code": "44261-6"}]},
               "subject": {"reference": "Patient/X"}, "effectiveDateTime": "2025-03-05",
               "valueInteger": 12}
        tables, _ = read_fhir([bundle(PATIENT, obs)], SETTINGS, "urn:site:registry")
        self.assertEqual(rows(tables["patient"])[0]["patient_id"], "R-42")
        self.assertEqual(rows(tables["scale_result"])[0]["patient_id"], "R-42")

    def test_reads_ndjson_from_a_bulk_export(self):
        ndjson = "\n".join(json.dumps(r) for r in (PATIENT, {**PATIENT, "id": "Y", "identifier": []}))
        tables, _ = read_fhir([ndjson], SETTINGS)
        self.assertEqual([r["patient_id"] for r in rows(tables["patient"])], ["X", "Y"])

    def test_rejects_something_that_isnt_fhir(self):
        with self.assertRaises(ValueError):
            read_fhir(['{"hello": "world"}'], SETTINGS)


class DateTests(unittest.TestCase):
    def test_utc_times_become_new_york_dates(self):
        # 1:30 a.m. UTC on 1 April is 9:30 p.m. on 31 March in New York: March's report.
        obs = {"resourceType": "Observation", "id": "o", "status": "final",
               "code": {"coding": [{"system": "http://loinc.org", "code": "44261-6"}]},
               "subject": {"reference": "Patient/X"}, "effectiveDateTime": "2025-04-01T01:30:00Z",
               "valueInteger": 12}
        tables, _ = read_fhir([bundle(PATIENT, obs)], SETTINGS)
        self.assertEqual(rows(tables["scale_result"])[0]["administered_date"], "2025-03-31")


class NewYorkWithoutTimeZoneDataTests(unittest.TestCase):
    """The browser has no time-zone database; the built-in New York rule must agree with it."""

    def test_matches_zoneinfo_across_daylight_saving(self):
        from datetime import datetime, timedelta, timezone
        from zoneinfo import ZoneInfo
        from calculator.fhir import _new_york
        zone = ZoneInfo("America/New_York")
        moment = datetime(2024, 1, 1, tzinfo=timezone.utc)
        while moment.year < 2027:  # every half hour across three years of transitions
            self.assertEqual(_new_york(moment), moment.astimezone(zone).replace(tzinfo=None), moment)
            moment += timedelta(minutes=30)


class CombineTests(unittest.TestCase):
    def test_same_phq9_from_registry_and_ehr_is_kept_once(self):
        registry = {"scale_result": "result_id,patient_id,administered_date,instrument,total_score\n"
                                    "S1,X,2025-03-05,phq9,12\n"}
        ehr = {"scale_result": "result_id,patient_id,administered_date,instrument,total_score,loinc\n"
                               "o1,X,2025-03-05,phq9,12,44261-6\n"
                               "o2,X,2025-03-20,phq9,9,44261-6\n"}
        merged = rows(combine(registry, ehr)["scale_result"])
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["loinc"], "44261-6")  # gap filled from the EHR


if __name__ == "__main__":
    unittest.main()
