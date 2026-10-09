"""Run the calculator on a directory of data-contract CSVs.

    python3 -m calculator DATA_DIR --month 2025-03
    python3 -m calculator DATA_DIR --month 2025-03 --json results.json
    python3 -m calculator workbook.xlsx --month 2025-03

DATA_DIR holds one CSV per data-contract table (patient.csv, coverage.csv, ...); or give
the reporting workbook instead. A missing table is treated as empty. The rules come from rules/calls.toml unless --rules says
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
from .report import summary
from .xlsx import read_workbook

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "rules", "calls.toml")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python3 -m calculator", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", help="directory of data-contract CSV files, or the reporting workbook (.xlsx)")
    parser.add_argument("--month", required=True, help="reporting month, YYYY-MM")
    parser.add_argument("--rules", default=DEFAULT_RULES, help="rules file (default: %(default)s)")
    parser.add_argument("--json", help="also write the full results to this file")
    args = parser.parse_args(argv)

    texts = {}
    if args.data.lower().endswith(".xlsx"):
        try:
            with open(args.data, "rb") as f:
                texts = read_workbook(f.read())
        except ValueError as e:
            parser.error(f"{args.data}: {e}")
    for path in glob.glob(os.path.join(args.data, "*.csv")):
        name = os.path.splitext(os.path.basename(path))[0]
        if name in TABLES:
            with open(path, newline="") as f:
                texts[name] = f.read()
    if not texts:
        parser.error(f"no data-contract tables in {args.data}")
    with open(args.rules) as f:
        settings = read_rules(f.read())

    try:
        results = calculate(read_tables(texts), settings, args.month)
    except (ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(summary(results))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(results, f, indent=2, default=str)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
