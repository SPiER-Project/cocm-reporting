"""Keep the guide's worked examples honest.

    python3 scripts/examples.py check           everything below; exit non-zero on a problem
    python3 scripts/examples.py sync            rewrite the example results shown in the docs
    python3 scripts/examples.py verify NAME     record that example NAME has been rechecked
    python3 scripts/examples.py verify --all

What check does:

1. Fixtures match the data contract. Every CSV in a fixture directory is a table from
   docs/reference/data-contract.md, with its columns, required values, allowed values
   and date formats.
2. The docs show the expected results. Pages mark each quoted result,
   <!--expect:example-caseload.m5-->7 of 8, 87.5%<!--/expect-->, and the results table is a
   generated block, <!--expects:example-caseload-results-->...<!--/expects-->. Percentages
   and weeks are computed from the counts in expected.toml using the rounding rule.
3. No example is stale. Each example in tests/examples.toml names the calls it depends
   on. If one of those calls has changed since the example was last verified (its values
   in rules/calls.toml, or the wording of its Call paragraph), check fails until someone
   reworks the example and runs verify.

There is no calculator yet. When there is, its tests run it on each fixture and compare
with expected.toml.
"""

import csv
import glob
import json
import os
import re
import sys
import tomllib
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import contract  # noqa: E402
import rules as R  # noqa: E402

ROOT = R.ROOT
REGISTRY = os.path.join(ROOT, "tests", "examples.toml")
LOCK = os.path.join(ROOT, "tests", "examples.lock.json")

METRICS = {
    "m1": ("1. Total enrollment", "metrics/01-total-enrollment.md"),
    "m2": ("2. Medicaid enrollment", "metrics/02-medicaid-enrollment.md"),
    "m3": ("3. Newly enrolled", "metrics/03-newly-enrolled.md"),
    "m4": ("4. Average duration of treatment", "metrics/04-average-duration-of-treatment.md"),
    "m5": ("5. Monthly contact rate", "metrics/05-monthly-contact-rate.md"),
    "m6": ("6. Improvement rate", "metrics/06-improvement-rate.md"),
    "m7": ("7. Remission rate", "metrics/07-remission-rate.md"),
    "m8": ("8. Psychiatric consultation rate", "metrics/08-psychiatric-consultation-rate.md"),
    "m9": ("9. Depression screening rate", "metrics/09-depression-screening-rate.md"),
    "m10": ("10. Depression screening yield", "metrics/10-depression-screening-yield.md"),
}

INLINE = re.compile(r"<!--expect:([\w\-]+)\.(m\d+)(?:\.(\w+))?-->(.*?)<!--/expect-->", re.S)
BLOCK = re.compile(r"(<!--expects:([\w\-]+)-results-->\n)(.*?)(<!--/expects-->)", re.S)


def load_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


# ------------------------------------------------------------------------- data contract


def contract_tables():
    """{table: {column: (type, required, allowed values or None)}} from the data contract."""
    return {name: {c["name"]: (c["type"], c["required"], set(c["allowed"]) if c["allowed"] else None)
                   for c in columns}
            for name, _, columns in contract.tables()}


def check_value(typ, value):
    if typ == "date":
        return re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None
    if typ == "int":
        return re.fullmatch(r"-?\d+", value) is not None
    if typ == "decimal":
        return re.fullmatch(r"-?\d+(\.\d+)?", value) is not None
    if typ == "bool":
        return value in ("true", "false")
    if typ == "YYYY-MM":
        return re.fullmatch(r"\d{4}-\d{2}", value) is not None
    return True


def check_fixture(directory, tables, errors):
    where = os.path.relpath(directory, ROOT)
    files = {os.path.splitext(os.path.basename(p))[0]: p
             for p in glob.glob(os.path.join(directory, "*.csv"))}
    for table in tables:
        if table not in files:
            errors.append(f"{where}: no {table}.csv (an empty file with the header will do)")
    for table, path in files.items():
        if table not in tables:
            errors.append(f"{where}/{table}.csv: not a data-contract table")
            continue
        cols = tables[table]
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames or []
            for c in header:
                if c not in cols:
                    errors.append(f"{where}/{table}.csv: column {c} isn't in the data contract")
            for c, (_, req, _) in cols.items():
                if req and c not in header:
                    errors.append(f"{where}/{table}.csv: missing required column {c}")
            for n, row in enumerate(reader, start=2):
                for c, value in row.items():
                    if c not in cols:
                        continue
                    typ, req, allowed = cols[c]
                    if value == "":
                        if req:
                            errors.append(f"{where}/{table}.csv:{n}: {c} is required")
                        continue
                    if typ == "string[]":
                        continue
                    if allowed is not None and value not in allowed:
                        errors.append(f"{where}/{table}.csv:{n}: {c} = {value!r} isn't allowed")
                    elif not check_value(typ, value):
                        errors.append(f"{where}/{table}.csv:{n}: {c} = {value!r} isn't a {typ}")


# ------------------------------------------------------------------------- results


def rounded(value, places):
    q = Decimal(1).scaleb(-places)
    return str(Decimal(value).quantize(q, rounding=ROUND_HALF_UP))


def results(expected, places):
    """{metric: {field: text}} for every metric in an expected.toml."""
    out = {}
    for m, e in expected.get("metrics", {}).items():
        if "count" in e:
            out[m] = {"display": str(e["count"])}
        elif "discharged_days" in e:
            days = e["discharged_days"]
            weeks = rounded(Decimal(sum(days)) / len(days) / 7, places)
            out[m] = {"display": f"{weeks} weeks"}
        else:
            num, den = e["numerator"], e["denominator"]
            pct = rounded(Decimal(num) * 100 / den, places) + "%"
            display = f"{num} of {den}, {pct}"
            if m == "m10":  # NYS asks for the count and the proportion
                display = f"{num} patient{'' if num == 1 else 's'}, {display}"
            out[m] = {"display": display, "percent": pct}
    return out


def results_table(name, computed):
    rows = ["| Metric | Result | Page |", "|---|---|---|"]
    for m, fields in computed.items():
        label, link = METRICS[m]
        rows.append(f"| {label} | {fields['display']} | [metric {m[1:]}]({link}) |")
    return "\n".join(rows) + "\n"


def render(text, computed, where, errors):
    def inline(m):
        name, metric, field = m.group(1), m.group(2), m.group(3) or "display"
        try:
            value = computed[name][metric][field]
        except KeyError:
            errors.append(f"{where}: unknown expected result {name}.{metric}.{field}")
            return m.group(0)
        suffix = f".{m.group(3)}" if m.group(3) else ""
        return f"<!--expect:{name}.{metric}{suffix}-->{value}<!--/expect-->"

    def block(m):
        name = m.group(2)
        if name not in computed:
            errors.append(f"{where}: unknown example {name}")
            return m.group(0)
        return m.group(1) + results_table(name, computed[name]) + m.group(4)

    return BLOCK.sub(block, INLINE.sub(inline, text))


# ------------------------------------------------------------------------- staleness


def current_fingerprints(rules, example):
    return {c: R.fingerprint(rules, c) for c in example["depends_on"]}


def load_lock():
    if not os.path.exists(LOCK):
        return {}
    return json.load(open(LOCK))


def write_lock(lock):
    with open(LOCK, "w") as f:
        json.dump(lock, f, indent=2, sort_keys=True)
        f.write("\n")


# ------------------------------------------------------------------------- commands


def main(argv):
    if len(argv) < 2 or argv[1] not in ("check", "sync", "verify"):
        print(__doc__)
        return 2
    rules = R.load()
    registry = load_toml(REGISTRY)["examples"]
    places = rules["calls"]["rounding"]["decimal_places"]
    errors, stale = [], []

    if argv[1] == "verify":
        names = list(registry) if argv[2:] == ["--all"] else argv[2:]
        if not names:
            print("verify needs an example name, or --all")
            return 2
        lock = load_lock()
        for name in names:
            if name not in registry:
                print(f"no example called {name}")
                return 2
            lock[name] = current_fingerprints(rules, registry[name])
            print(f"verified {name}")
        write_lock(lock)
        return 0

    for name, ex in registry.items():
        for c in ex["depends_on"]:
            if c not in rules["calls"]:
                errors.append(f"tests/examples.toml: {name} depends on unknown call {c}")
        for p in ex["pages"]:
            if not os.path.exists(os.path.join(ROOT, p)):
                errors.append(f"tests/examples.toml: {name} lists missing page {p}")
    if errors:
        for e in errors:
            print(e)
        return 1

    tables = contract_tables()
    computed = {}
    for name, ex in registry.items():
        if "fixture" in ex:
            directory = os.path.join(ROOT, ex["fixture"])
            check_fixture(directory, tables, errors)
            computed[name] = results(load_toml(os.path.join(directory, "expected.toml")), places)

    changed = []
    for path in R.docs():
        where = os.path.relpath(path, ROOT)
        before = open(path).read()
        after = render(before, computed, where, errors)
        if after != before:
            changed.append(where)
            if argv[1] == "sync":
                open(path, "w").write(after)

    lock = load_lock()
    for name, ex in registry.items():
        recorded = lock.get(name, {})
        moved = [c for c, fp in current_fingerprints(rules, ex).items() if recorded.get(c) != fp]
        if moved:
            stale.append((name, ex, moved))

    for e in errors:
        print(e)
    if argv[1] == "sync":
        print(f"synced {len(changed)} file(s)" + (": " + ", ".join(changed) if changed else ""))
    else:
        for where in changed:
            print(f"{where}: example results out of date; run python3 scripts/examples.py sync")
    for name, ex, moved in stale:
        reason = ("it has never been verified" if name not in lock else
                  f"these calls changed since it was last verified: {', '.join(moved)}")
        print(f"{name}: stale; {reason}. Recheck the example on {', '.join(ex['pages'])}"
              + (f" and its fixture {ex['fixture']}" if "fixture" in ex else "")
              + f", then run python3 scripts/examples.py verify {name}")
    if argv[1] == "check":
        print(f"{len(registry)} examples; {len(computed)} fixtures; {len(changed)} file(s) out "
              f"of date; {len(stale)} stale; {len(errors)} error(s)")
        return 1 if errors or changed or stale else 0
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
