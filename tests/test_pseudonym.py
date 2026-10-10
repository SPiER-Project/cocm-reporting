"""Tests for pseudonymous patient ids.

    python3 -m unittest discover tests
"""

import base64
import csv
import glob
import hashlib
import hmac
import io
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from calculator import calculate, read_rules, read_tables  # noqa: E402
from calculator.data import combine  # noqa: E402
from calculator.pseudonym import new_key, normalize, pseudonym, pseudonymize, read_key  # noqa: E402

# The published test vector (docs/collecting/overview.md#one-patient-id): anyone
# implementing the same scheme elsewhere can check their output against it.
TEST_KEY = "cocm-pseudonym-key-v1:AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="
KEY = read_key(TEST_KEY)

with open(os.path.join(ROOT, "rules", "calls.toml")) as f:
    SETTINGS = read_rules(f.read())


def rows(text):
    return list(csv.DictReader(io.StringIO(text)))


class SchemeTests(unittest.TestCase):
    def test_published_test_vector(self):
        self.assertEqual(pseudonym(KEY, "123"), "p-47cvhcslcvte5vth")
        self.assertEqual(pseudonym(KEY, "MRN-0042"), "p-vwwfuzieeoipmduc")

    def test_it_is_hmac_sha256_of_the_normalized_mrn(self):
        digest = hmac.new(KEY, b"123", hashlib.sha256).digest()
        self.assertEqual(pseudonym(KEY, "123"), "p-" + base64.b32encode(digest).decode().lower()[:16])

    def test_formats_of_the_same_mrn_agree(self):
        same = {pseudonym(KEY, m) for m in ("123", "00123", " 123 ", "1-2-3", "000.123")}
        self.assertEqual(len(same), 1)
        self.assertEqual(normalize("mrn-0042"), "MRN0042")  # letters keep their zeros

    def test_different_mrns_and_keys_differ(self):
        self.assertNotEqual(pseudonym(KEY, "123"), pseudonym(KEY, "124"))
        other = read_key(new_key())
        self.assertNotEqual(pseudonym(KEY, "123"), pseudonym(other, "123"))

    def test_new_keys_are_random_and_readable(self):
        a, b = new_key(), new_key()
        self.assertNotEqual(a, b)
        self.assertEqual(len(read_key(a)), 32)

    def test_rejects_a_bad_key(self):
        for text in ("", "secret", "cocm-pseudonym-key-v1:short", "cocm-pseudonym-key-v1:!!!"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                read_key(text)


class TableTests(unittest.TestCase):
    def test_registry_and_ehr_join_after_pseudonymizing(self):
        registry = {"patient": "patient_id,birth_date\n00123,1980-01-01\n",
                    "scale_result": "result_id,patient_id,administered_date,instrument,total_score\n"
                                    "S1,00123,2025-03-05,phq9,12\n"}
        ehr = {"patient": "patient_id,birth_date\n123,1980-01-01\n",
               "scale_result": "result_id,patient_id,administered_date,instrument,total_score\n"
                               "o1,123,2025-03-05,phq9,12\n"}
        merged = combine(pseudonymize(registry, TEST_KEY)[0], pseudonymize(ehr, TEST_KEY)[0])
        self.assertEqual([r["patient_id"] for r in rows(merged["patient"])], ["p-47cvhcslcvte5vth"])
        self.assertEqual(len(rows(merged["scale_result"])), 1)

    def test_crosswalk_lists_each_original_once(self):
        tables = {"patient": "patient_id,birth_date\nA,1980-01-01\nB,1990-01-01\n",
                  "contact": "contact_id,patient_id\nC1,A\nC2,A\n"}
        _, crosswalk = pseudonymize(tables, TEST_KEY)
        self.assertEqual([o for o, _ in crosswalk], ["A", "B"])

    def test_results_dont_change(self):
        directory = os.path.join(ROOT, "tests", "fixtures", "example-caseload")
        texts = {}
        for path in glob.glob(os.path.join(directory, "*.csv")):
            with open(path, newline="") as f:
                texts[os.path.splitext(os.path.basename(path))[0]] = f.read()
        before = calculate(read_tables(texts), SETTINGS, "2025-03")["metrics"]
        after = calculate(read_tables(pseudonymize(texts, TEST_KEY)[0]), SETTINGS, "2025-03")["metrics"]
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
