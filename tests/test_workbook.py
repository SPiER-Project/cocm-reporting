"""Tests for the reporting workbook: the template builder and the reader.

    python3 -m unittest discover tests
"""

import base64
import glob
import io
import json
import os
import sys
import unittest
import zipfile
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import build_workbook  # noqa: E402
import contract  # noqa: E402
from calculator import calculate, read_rules, read_tables  # noqa: E402
from calculator.web import workbook as web_workbook  # noqa: E402
from calculator.xlsx import read_workbook  # noqa: E402

FIXTURE = os.path.join(ROOT, "tests", "fixtures", "example-caseload")


class TemplateTests(unittest.TestCase):
    def test_blank_template_has_every_contract_table_and_column(self):
        tables = read_workbook(build_workbook.workbook())
        for name, _, columns in contract.tables():
            with self.subTest(table=name):
                header = tables[name].splitlines()[0].split(",")
                self.assertEqual(header, [c["name"] for c in columns])
                self.assertEqual(len(tables[name].splitlines()), 1)  # no data rows

    def test_example_workbook_round_trips_the_fixture_exactly(self):
        tables = read_workbook(build_workbook.workbook(build_workbook.example_data()))
        for path in glob.glob(os.path.join(FIXTURE, "*.csv")):
            name = os.path.splitext(os.path.basename(path))[0]
            with self.subTest(table=name), open(path, newline="") as f:
                self.assertEqual(tables[name], f.read())

    def test_build_is_reproducible(self):
        self.assertEqual(build_workbook.workbook(), build_workbook.workbook())

    def test_published_workbooks_are_current(self):
        for path, content in build_workbook.outputs().items():
            with self.subTest(path=os.path.relpath(path, ROOT)), open(path, "rb") as f:
                self.assertEqual(f.read(), content, "run python3 scripts/build_workbook.py")


def excel_style_workbook():
    """A workbook saved the way Excel saves: shared strings, dates as serial numbers,
    booleans as boolean cells, a typed US-style date, and cells out of order."""
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    strings = ["review_id", "patient_id", "review_date", "recommendation_documented",
               "R1", "P1", "R2", "P2"]
    serial = (date(2025, 3, 5) - date(1899, 12, 30)).days
    sheet = (f'<worksheet xmlns="{main}"><sheetData>'
             '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c>'
             '<c r="C1" t="s"><v>2</v></c><c r="D1" t="s"><v>3</v></c></row>'
             f'<row r="2"><c r="B2" t="s"><v>5</v></c><c r="A2" t="s"><v>4</v></c>'
             f'<c r="C2" s="1"><v>{serial}</v></c><c r="D2" t="b"><v>1</v></c></row>'
             '<row r="3"><c r="A3" t="s"><v>6</v></c><c r="B3" t="s"><v>7</v></c>'
             '<c r="C3" t="s"><v>8</v></c><c r="D3" t="str"><v>No</v></c></row>'
             '<row r="4"/></sheetData></worksheet>')
    shared = (f'<sst xmlns="{main}">' + "".join(f"<si><t>{s}</t></si>" for s in strings)
              + "<si><r><t>2/26/</t></r><r><t>2025</t></r></si></sst>")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("xl/workbook.xml", f'<workbook xmlns="{main}" xmlns:r="{rel}"><sheets>'
                   '<sheet name="Psych_Review" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   f'<Relationship Id="rId1" Type="{rel}/worksheet" Target="/xl/worksheets/sheet1.xml"/>'
                   '</Relationships>')
        z.writestr("xl/sharedStrings.xml", shared)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    return buf.getvalue()


class ReaderTests(unittest.TestCase):
    def test_reads_an_excel_style_workbook(self):
        tables = read_workbook(excel_style_workbook())
        self.assertEqual(tables["psych_review"].splitlines(), [
            "review_id,patient_id,review_date,recommendation_documented",
            "R1,P1,2025-03-05,true",
            "R2,P2,2025-02-26,false",
        ])

    def test_rejects_a_file_that_isnt_a_workbook(self):
        with self.assertRaises(ValueError):
            read_workbook(b"patient_id,birth_date\n")

    def test_the_example_workbook_gives_the_expected_results(self):
        with open(os.path.join(ROOT, "rules", "calls.toml")) as f:
            settings = read_rules(f.read())
        tables = read_workbook(build_workbook.workbook(build_workbook.example_data()))
        metrics = calculate(read_tables(tables), settings, "2025-03")["metrics"]
        self.assertEqual(metrics["m5"]["percent"], "87.5")
        self.assertEqual(metrics["m4"]["weeks"], "18.7")

    def test_web_entry_point(self):
        data = base64.b64encode(build_workbook.workbook(build_workbook.example_data())).decode()
        got = json.loads(web_workbook(data))
        self.assertEqual(len(got["texts"]), 8)
        self.assertIn("error", json.loads(web_workbook(base64.b64encode(b"nope").decode())))


if __name__ == "__main__":
    unittest.main()
