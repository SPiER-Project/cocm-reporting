"""Tests for the calculator.

    python3 -m unittest discover tests

The fixture tests run the calculator on each fixture in tests/fixtures and compare with
its expected.toml, metric by metric and then patient by patient. The rule tests check
the edges of individual calls on small, made-up tables.
"""

import glob
import os
import sys
import tomllib
import unittest
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from calculator import calculate, read_rules, read_tables  # noqa: E402
from calculator.data import combine  # noqa: E402
from calculator.fhir import read_fhir  # noqa: E402
from calculator.compute import months_back, rate  # noqa: E402

with open(os.path.join(ROOT, "rules", "calls.toml")) as f:
    RULES_TEXT = f.read()
SETTINGS = read_rules(RULES_TEXT)


def load_fixture(directory):
    """A fixture's tables, from CSV files or from FHIR resources (.json, .ndjson)."""
    texts = {}
    for path in glob.glob(os.path.join(directory, "*.csv")):
        with open(path, newline="") as f:
            texts[os.path.splitext(os.path.basename(path))[0]] = f.read()
    fhir = [open(p).read() for p in sorted(glob.glob(os.path.join(directory, "*.json"))
                                           + glob.glob(os.path.join(directory, "*.ndjson")))]
    if fhir:
        texts = combine(texts, read_fhir(fhir, SETTINGS)[0])
    return read_tables(texts)


class FixtureTests(unittest.TestCase):
    def test_fixtures(self):
        fixtures = sorted(glob.glob(os.path.join(ROOT, "tests", "fixtures", "*")))
        self.assertTrue(fixtures, "no fixtures found")
        for directory in fixtures:
            name = os.path.basename(directory)
            with open(os.path.join(directory, "expected.toml"), "rb") as f:
                expected = tomllib.load(f)
            results = calculate(load_fixture(directory), SETTINGS, expected["reporting_month"])
            for metric, want in expected["metrics"].items():
                got = results["metrics"][metric]
                for key, value in want.items():
                    with self.subTest(fixture=name, metric=metric, field=key):
                        if key == "discharged_days":
                            self.assertEqual(sorted(got[key]), sorted(value))
                        else:
                            self.assertEqual(got[key], value)
            for patient, facts in expected.get("patients", {}).items():
                got = results["patients"].get(patient)
                with self.subTest(fixture=name, patient=patient):
                    self.assertIsNotNone(got, f"{patient} missing from the results")
                for key, value in facts.items():
                    with self.subTest(fixture=name, patient=patient, fact=key):
                        self.assertEqual(got.get(key), value)


# Small tables for testing one rule at a time -----------------------------------------


def tables(**rows):
    """Tables from lists of row dicts, with dates as ISO strings."""
    out = {t: [] for t in ("patient", "coverage", "cocm_episode", "contact", "scale_result",
                           "psych_review", "practice_visit", "site_month")}
    for table, items in rows.items():
        for r in items:
            out[table].append({k: date.fromisoformat(v) if k.endswith("_date") and v else v
                               for k, v in r.items()})
    return out


def episode(start, scale="phq9", discharge=None, pid="X"):
    return {"episode_id": "E" + pid, "patient_id": pid, "enrollment_date": start,
            "enrollment_source": "registry", "primary_condition": "depression",
            "primary_scale": scale, "primary_scale_source": "recorded",
            "discharge_date": discharge, "discharge_reason": None}


def contact(day, kind="treatment", pid="X", n=[0]):
    n[0] += 1
    return {"contact_id": f"C{n[0]}", "patient_id": pid, "contact_date": day,
            "staff_role": "bhcm", "contact_kind": kind, "modality": "phone"}


def score(day, value, instrument="phq9", pid="X", n=[0]):
    n[0] += 1
    return {"result_id": f"S{n[0]:03}", "patient_id": pid, "administered_date": day,
            "instrument": instrument, "total_score": value, "vanderbilt_symptom_count": None}


MEDICAID = [{"patient_id": "X", "payer_category": "medicaid_ffs", "start_date": "2024-01-01",
             "end_date": None}]


class RuleTests(unittest.TestCase):
    def run_month(self, t, month="2025-03"):
        return calculate(t, SETTINGS, month)

    def test_inactivity_contact_on_day_90_keeps_patient_enrolled(self):
        # Last contact 10 Dec; 10 Mar is day 90. A contact that day isn't a 90-day gap.
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-10")],
                   contact=[contact("2024-12-10"), contact("2025-03-10")])
        r = self.run_month(t)
        self.assertIsNone(r["patients"]["X"]["effective_discharge_date"])

    def test_inactivity_discharges_on_day_90(self):
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-10")],
                   contact=[contact("2024-12-10"), contact("2025-03-11")])
        r = self.run_month(t)
        self.assertEqual(r["patients"]["X"]["effective_discharge_date"], "2025-03-10")

    def test_outreach_isnt_a_clinical_contact(self):
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2025-03-01")],
                   contact=[contact("2025-03-05", kind="outreach_attempt")],
                   scale_result=[score("2025-03-05", 15)])
        r = self.run_month(t)
        self.assertFalse(r["patients"]["X"]["active_treatment"])

    def test_fifty_percent_boundary_counts(self):
        # GAD-7 from 20 to exactly 10: half the baseline, so improved.
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-01", scale="gad7")],
                   contact=[contact(d) for d in ("2024-12-01", "2025-01-15", "2025-02-15", "2025-03-15")],
                   scale_result=[score("2024-12-01", 20, "gad7"), score("2025-03-15", 10, "gad7")])
        self.assertTrue(self.run_month(t)["patients"]["X"]["improved"])

    def test_screening_score_before_enrollment_isnt_the_baseline(self):
        # A PHQ-9 of 9 before enrollment would make the baseline not elevated.
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2025-03-03")],
                   contact=[contact("2025-03-03")],
                   scale_result=[score("2025-02-20", 9), score("2025-03-03", 15)])
        self.assertTrue(self.run_month(t)["patients"]["X"]["elevated_baseline"])

    def test_remission_needs_a_score_this_month(self):
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-01")],
                   contact=[contact(d) for d in ("2024-12-01", "2025-01-15", "2025-02-15", "2025-03-15")],
                   scale_result=[score("2024-12-01", 15), score("2025-02-15", 3)])
        r = self.run_month(t)
        self.assertTrue(r["patients"]["X"]["improved"])      # carried forward
        self.assertFalse(r["patients"]["X"]["in_remission"])  # not carried forward

    def test_paired_forms_either_form_counts(self):
        # SCARED: the child form barely moves; the caregiver form halves. Improved.
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-01", scale="scared_child")],
                   contact=[contact(d) for d in ("2024-12-01", "2025-01-15", "2025-02-15", "2025-03-15")],
                   scale_result=[score("2024-12-01", 30, "scared_child"), score("2024-12-02", 30, "scared_parent"),
                                 score("2025-03-15", 28, "scared_child"), score("2025-03-15", 15, "scared_parent")])
        self.assertTrue(self.run_month(t)["patients"]["X"]["improved"])

    def test_form_without_a_threshold_cant_count(self):
        # Child SMFQ barely moves; the parent form improves by 6 against its own baseline.
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-01", scale="smfq_child")],
                   contact=[contact(d) for d in ("2024-12-01", "2025-01-15", "2025-02-15", "2025-03-15")],
                   scale_result=[score("2024-12-01", 16, "smfq_child"), score("2024-12-01", 14, "smfq_parent"),
                                 score("2025-03-15", 15, "smfq_child"), score("2025-03-15", 8, "smfq_parent")])
        # The parent form has no elevated threshold yet, so it can't count: not improved.
        self.assertFalse(self.run_month(t)["patients"]["X"]["improved"])

    def test_empty_denominator_has_no_value(self):
        self.assertIsNone(rate(0, 0, 1))
        r = self.run_month(tables())
        self.assertIsNone(r["metrics"]["m5"]["percent"])
        self.assertIsNone(r["metrics"]["m4"]["weeks"])

    def test_rounding_is_half_up(self):
        self.assertEqual(rate(1, 8, 1), "12.5")
        self.assertEqual(rate(1, 16, 1), "6.3")   # 6.25

    def test_99211_isnt_a_qualifying_visit(self):
        t = tables(patient=[{"patient_id": "X", "birth_date": "1980-01-01"}],
                   practice_visit=[{"visit_id": "V1", "patient_id": "X", "visit_date": "2025-03-05",
                                    "provider_category": "primary_care", "billing_codes": ["99211"],
                                    "modality": "in_person"}])
        self.assertEqual(self.run_month(t)["metrics"]["m9"]["denominator"], 0)

    def test_age_floor_is_age_on_the_visit_date(self):
        # Turns 12 on 10 March; visit on 9 March doesn't count, on 10 March does.
        def visit(day):
            return tables(patient=[{"patient_id": "X", "birth_date": "2013-03-10"}],
                          practice_visit=[{"visit_id": "V1", "patient_id": "X", "visit_date": day,
                                           "provider_category": "primary_care",
                                           "billing_codes": ["99213"], "modality": "in_person"}])
        self.assertEqual(self.run_month(visit("2025-03-09"))["metrics"]["m9"]["denominator"], 0)
        self.assertEqual(self.run_month(visit("2025-03-10"))["metrics"]["m9"]["denominator"], 1)

    def test_phq_a_counts_as_phq9_for_initial(self):
        t = tables(patient=[{"patient_id": "X"}],
                   scale_result=[score("2024-06-01", 5, "phq_a"), score("2025-03-05", 12, "phq9")])
        self.assertFalse(self.run_month(t)["patients"]["X"]["initial_phq9"])

    def test_phq_a_as_the_primary_scale(self):
        t = tables(patient=[{"patient_id": "X"}], coverage=MEDICAID,
                   cocm_episode=[episode("2024-12-01", scale="phq_a")],
                   contact=[contact(d) for d in ("2024-12-01", "2025-01-15", "2025-02-15", "2025-03-15")],
                   scale_result=[score("2024-12-01", 15, "phq_a"), score("2025-03-15", 6, "phq_a")])
        self.assertTrue(self.run_month(t)["patients"]["X"]["improved"])

    def test_months_back_wraps_years(self):
        self.assertEqual(months_back(date(2025, 3, 1), 11), date(2024, 4, 1))
        self.assertEqual(months_back(date(2024, 12, 1), -1), date(2025, 1, 1))


class WebEntryPointTests(unittest.TestCase):
    """The browser page passes strings to calculator.web.run and gets JSON back."""

    def test_runs_the_example_caseload(self):
        import json
        from calculator.web import run
        directory = os.path.join(ROOT, "tests", "fixtures", "example-caseload")
        texts = {}
        for path in glob.glob(os.path.join(directory, "*.csv")):
            with open(path, newline="") as f:
                texts[os.path.splitext(os.path.basename(path))[0]] = f.read()
        results = json.loads(run(json.dumps(texts), RULES_TEXT, "2025-03"))
        values = {row["metric"]: row["value"] for row in results["rows"]}
        self.assertEqual(values["5"], "7 of 8, 87.5%")
        self.assertEqual(values["4"], "18.7 weeks")

    def test_reports_bad_input_as_an_error(self):
        import json
        from calculator.web import run
        self.assertIn("error", json.loads(run(json.dumps({"visits": ""}), RULES_TEXT, "2025-03")))


if __name__ == "__main__":
    unittest.main()
