"""Run the calculator on a directory of data-contract CSVs.

    python3 -m calculator DATA_DIR --month 2025-03
    python3 -m calculator DATA_DIR --month 2025-03 --json results.json
    python3 -m calculator workbook.xlsx --month 2025-03
    python3 -m calculator workbook.xlsx ehr-export/ --month 2025-03

Each input is a directory of data-contract CSVs (patient.csv, coverage.csv, ...), the
reporting workbook, or FHIR resources: .json Bundles or .ndjson from a bulk export, as
files or in a directory. Several inputs are combined, so the CoCM half can come from the
workbook and the EHR half from FHIR. A missing table is treated as empty. The rules come from rules/calls.toml unless --rules says
otherwise. Results print as a summary; --json also writes everything, including the
patient-level list of who fell out of each numerator. That list identifies patients by
their pseudonymous id; keep it at the site.
"""

import argparse
import glob
import json
import os
import sys

from . import TABLES, calculate, read_rules, read_tables
from .data import combine
from .fhir import read_fhir
from .report import summary
from .xlsx import read_workbook

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "rules", "calls.toml")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python3 -m calculator", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", nargs="+",
                        help="a directory of CSVs or FHIR files, the workbook (.xlsx), or FHIR files")
    parser.add_argument("--fhir-patient-identifier", metavar="SYSTEM",
                        help="use the Patient.identifier with this system as the patient id "
                             "(default: Patient.id), so FHIR data joins the registry's")
    parser.add_argument("--month", required=True, help="reporting month, YYYY-MM")
    parser.add_argument("--rules", default=DEFAULT_RULES, help="rules file (default: %(default)s)")
    parser.add_argument("--json", help="also write the full results to this file")
    args = parser.parse_args(argv)

    with open(args.rules) as f:
        rules_text = f.read()
    settings = read_rules(rules_text)
    sources, fhir_texts = [], []
    for item in args.data:
        paths = sorted(glob.glob(os.path.join(item, "*"))) if os.path.isdir(item) else [item]
        csvs = {}
        for path in paths:
            lower = path.lower()
            if lower.endswith(".xlsx"):
                try:
                    with open(path, "rb") as f:
                        sources.append(read_workbook(f.read()))
                except ValueError as e:
                    parser.error(f"{path}: {e}")
            elif lower.endswith((".json", ".ndjson")):
                with open(path) as f:
                    fhir_texts.append(f.read())
            elif lower.endswith(".csv"):
                name = os.path.splitext(os.path.basename(path))[0]
                if name in TABLES:
                    with open(path, newline="") as f:
                        csvs[name] = f.read()
        if csvs:
            sources.append(csvs)
    notes = []
    if fhir_texts:
        try:
            tables, notes = read_fhir(fhir_texts, settings, args.fhir_patient_identifier)
        except ValueError as e:
            parser.error(f"FHIR: {e}")
        sources.append(tables)
    texts = combine(*sources)
    if not texts:
        parser.error("no data-contract tables or FHIR resources in " + ", ".join(args.data))

    try:
        results = calculate(read_tables(texts), settings, args.month)
    except (ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    results["disclosures"] += notes
    print(summary(results))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2, default=str)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
