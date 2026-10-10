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
import json
import os
import sys

from . import calculate, read_rules, read_tables
from .data import combine
from .inputs import read_inputs
from .pseudonym import pseudonymize
from .report import summary

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
    parser.add_argument("--pseudonym-key", metavar="KEY_FILE",
                        help="replace patient ids with pseudonyms made with this key first, so "
                             "the results name no MRNs (see python3 -m calculator.pseudonymize)")
    args = parser.parse_args(argv)

    with open(args.rules) as f:
        rules_text = f.read()
    settings = read_rules(rules_text)
    try:
        sources, notes = read_inputs(args.data, settings, args.fhir_patient_identifier)
    except ValueError as e:
        parser.error(str(e))
    if args.pseudonym_key:
        with open(args.pseudonym_key) as f:
            key = f.read()
        try:
            sources = [pseudonymize(s, key)[0] for s in sources]
        except ValueError as e:
            parser.error(str(e))
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
