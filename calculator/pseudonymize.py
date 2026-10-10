"""Replace patient ids with pseudonyms, consistently across sources.

    python3 -m calculator.pseudonymize new-key site.key
    python3 -m calculator.pseudonymize INPUT... --key site.key --out DIR [--crosswalk FILE]

new-key writes a new random key. Make it once, keep it somewhere safe at the site, and
use the same key every month: a new key gives every patient a new pseudonym.

The second form reads the inputs (CSV directories, workbooks, FHIR files), replaces each
patient id with its pseudonym, combines them, and writes one CSV per data-contract table
to DIR, ready for the calculator or to share. --crosswalk also writes which original id
became which pseudonym; keep it at the site with the key.

Patient ids should be the MRN, the one id the registry and the EHR share. For FHIR, use
--fhir-patient-identifier to say which Patient.identifier holds the MRN.
"""

import argparse
import os
import sys

from .data import combine, read_rules
from .inputs import read_inputs
from .pseudonym import crosswalk_csv, new_key, pseudonymize

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "rules", "calls.toml")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["new-key"]:
        if len(argv) != 2:
            print("usage: python3 -m calculator.pseudonymize new-key KEY_FILE", file=sys.stderr)
            return 2
        if os.path.exists(argv[1]):
            print(f"error: {argv[1]} already exists; a new key would change every pseudonym",
                  file=sys.stderr)
            return 1
        with open(argv[1], "x") as f:
            f.write(new_key())
        os.chmod(argv[1], 0o600)
        print(f"wrote a new key to {argv[1]}. Keep it at the site, and use it every month.")
        return 0

    parser = argparse.ArgumentParser(prog="python3 -m calculator.pseudonymize", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", nargs="+", help="CSV directories, workbooks (.xlsx) or FHIR files")
    parser.add_argument("--key", required=True, help="the site's key file")
    parser.add_argument("--out", required=True, help="directory to write the pseudonymized CSVs to")
    parser.add_argument("--crosswalk", help="also write original id -> pseudonym to this file")
    parser.add_argument("--fhir-patient-identifier", metavar="SYSTEM",
                        help="the Patient.identifier system that holds the MRN")
    parser.add_argument("--rules", default=DEFAULT_RULES, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    with open(args.rules) as f:
        settings = read_rules(f.read())
    with open(args.key) as f:
        key = f.read()
    try:
        sources, notes = read_inputs(args.data, settings, args.fhir_patient_identifier)
        done = [pseudonymize(s, key) for s in sources]
    except ValueError as e:
        parser.error(str(e))
    tables = combine(*[t for t, _ in done])
    os.makedirs(args.out, exist_ok=True)
    for table, text in tables.items():
        with open(os.path.join(args.out, f"{table}.csv"), "w", newline="") as f:
            f.write(text)
    rows = sorted({r for _, cw in done for r in cw})
    if args.crosswalk:
        with open(args.crosswalk, "w", newline="") as f:
            f.write(crosswalk_csv(rows))
        os.chmod(args.crosswalk, 0o600)
    patients = len({p for _, p in rows})
    print(f"wrote {len(tables)} tables to {args.out}: {patients} patients, "
          f"from {len(rows)} distinct original ids")
    for note in notes:
        print(f"  - {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
