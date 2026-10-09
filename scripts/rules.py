"""Keep the docs in step with rules/calls.toml.

    python3 scripts/rules.py sync     rewrite the values and tables shown in the docs
    python3 scripts/rules.py check    exit non-zero if the docs and rules disagree

The docs mark the places that show a rule's value:

    Inline:  <!--rule:inactivity-discharge.days-->90<!--/rule-->
             The path is a call's slug and key, or a top-level table and key
             (extraction.phq_history_months). Dict values are read by a further key:
             elevated-baseline.thresholds.phq9.at_or_above
    Block:   <!--rules:elevated-baseline-table-->
             ...generated table...
             <!--/rules-->

HTML comments don't render, so readers see only the value. Edit the value in
rules/calls.toml, never between the markers.
"""

import glob
import os
import re
import sys
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = os.path.join(ROOT, "rules", "calls.toml")
CALLS_PAGE = os.path.join(ROOT, "docs", "reference", "our-calls.md")

FIRMNESS = {
    "nys-says": "NYS says",
    "our-call": "Our call",
    "needs-clinical-sign-off": "Needs clinical sign-off",
}
STATUS = {"proposed": "Proposed", "adopted": "Adopted"}
APPROVAL = {"needed": "Needed", "approved": "Approved", "confirmed-by-nys": "Confirmed by NYS"}

INLINE = re.compile(r"<!--rule:([\w.\-]+)-->(.*?)<!--/rule-->", re.S)
BLOCK = re.compile(r"(<!--rules:([\w\-]+)-->\n)(.*?)(<!--/rules-->)", re.S)


def load():
    with open(RULES, "rb") as f:
        return tomllib.load(f)


def slug(heading):
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


# ------------------------------------------------------------------------- validation


def validate(rules):
    errors = []
    calls = rules.get("calls", {})
    for name, call in calls.items():
        for key in ("title", "group", "firmness", "status", "approval"):
            if key not in call:
                errors.append(f"rules: {name} has no {key}")
        if call.get("firmness") not in FIRMNESS:
            errors.append(f"rules: {name} has unknown firmness {call.get('firmness')!r}")
        if call.get("status") not in STATUS:
            errors.append(f"rules: {name} has unknown status {call.get('status')!r}")
        if call.get("approval") not in APPROVAL:
            errors.append(f"rules: {name} has unknown approval {call.get('approval')!r}")
        if "title" in call and slug(call["title"]) != name:
            errors.append(f"rules: {name}'s title {call['title']!r} doesn't match its slug")
    headings = {slug(h) for h in re.findall(r"^### (.*)$", open(CALLS_PAGE).read(), re.M)}
    for name in calls:
        if name not in headings:
            errors.append(f"our-calls.md: no '### ' heading for the call {name}")
    for name in headings - set(calls):
        errors.append(f"rules: our-calls.md has a call {name} that rules/calls.toml lacks")
    return errors


# ------------------------------------------------------------------------- rendering


THRESHOLD_KEYS = ("at_or_above", "below", "symptom_count_below")


def lookup(rules, path):
    parts = path.split(".")
    node = rules["calls"] if parts[0] in rules["calls"] else rules
    for i, part in enumerate(parts):
        if isinstance(node, dict) and part not in node and i == len(parts) - 1 \
                and part in THRESHOLD_KEYS:
            return "not set"  # a threshold that hasn't been set yet
        if not isinstance(node, dict) or part not in node:
            raise KeyError(path)
        node = node[part]
    return node


def fmt(value, key=""):
    if key.endswith("firmness"):
        return FIRMNESS[value]
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list):
        return ", ".join(fmt(v) for v in value)
    return str(value)


def codes(items):
    return ", ".join(c.replace("-", "–") for c in items) or "To be confirmed"


def scale_name(rules, key):
    return rules["scales"][key]


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += [("| " + " | ".join(r) + " |").replace("|  |", "| |").replace("|  |", "| |")
            for r in rows]
    return "\n".join(out) + "\n"


def calls_summary(rules):
    rows, group = [], None
    for name, c in rules["calls"].items():
        if c["group"] != group:
            group = c["group"]
            rows.append([f"**{group}**", "", "", ""])
        firmness = FIRMNESS[c["firmness"]] + c.get("firmness_note", "")
        rows.append([f"[{c['title']}](#{name})", firmness, STATUS[c["status"]],
                     APPROVAL[c["approval"]]])
    return table(["Call", "Firmness", "Status", "Approval"], rows)


def elevated_table(rules):
    rows = []
    for key, t in rules["calls"]["elevated-baseline"]["thresholds"].items():
        value = str(t["at_or_above"]) if "at_or_above" in t else "not yet set"
        rows.append([scale_name(rules, key), value, FIRMNESS[t["firmness"]]])
    return table(["Scale", "Elevated at or above", "Firmness"], rows)


def remission_value(t):
    if "below" in t:
        return str(t["below"])
    if "symptom_count_below" in t:
        return f"fewer than {t['symptom_count_below']} symptom items rated 2 or 3"
    return "not yet set"


def remission_table(rules):
    rows = []
    for key, t in rules["calls"]["remission-thresholds"]["thresholds"].items():
        rows.append([scale_name(rules, key), remission_value(t), FIRMNESS[t["firmness"]]])
    return table(["Scale", "Remission below", "Firmness"], rows)


def primary_scale_table(rules):
    rows = []
    for m in rules["calls"]["primary-scale"]["default_mapping"]:
        scales = " or ".join(scale_name(rules, s) for s in m["scales"])
        if "note" in m:
            scales += f"; {m['note']}"
        rows.append([m["diagnosis"], scales])
    return table(["Primary diagnosis", "Primary scale"], rows)


def visit_codes_table(rules):
    rows = [[v["visit"], codes(v["codes"])]
            for v in rules["calls"]["who-should-be-screened"]["visit_types"]]
    return table(["Visit", "Codes"], rows)


BLOCKS = {
    "calls-summary": calls_summary,
    "elevated-baseline-table": elevated_table,
    "remission-thresholds-table": remission_table,
    "primary-scale-table": primary_scale_table,
    "visit-codes-table": visit_codes_table,
}


def render(text, rules, where, errors):
    def inline(m):
        path = m.group(1)
        try:
            value = lookup(rules, path)
        except KeyError:
            errors.append(f"{where}: unknown rule {path}")
            return m.group(0)
        if isinstance(value, dict):
            errors.append(f"{where}: rule {path} is a table, not a value")
            return m.group(0)
        return f"<!--rule:{path}-->{fmt(value, path)}<!--/rule-->"

    def block(m):
        name = m.group(2)
        if name not in BLOCKS:
            errors.append(f"{where}: unknown block {name}")
            return m.group(0)
        return m.group(1) + BLOCKS[name](rules) + m.group(4)

    return BLOCK.sub(block, INLINE.sub(inline, text))


# ------------------------------------------------------------------------- commands


def docs():
    paths = glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
    return sorted(p for p in paths if os.sep + "archive" + os.sep not in p)


def main(argv):
    if len(argv) != 2 or argv[1] not in ("sync", "check"):
        print(__doc__)
        return 2
    rules = load()
    errors = validate(rules)
    changed = []
    for path in docs():
        where = os.path.relpath(path, ROOT)
        before = open(path).read()
        after = render(before, rules, where, errors)
        if after != before:
            changed.append(where)
            if argv[1] == "sync":
                open(path, "w").write(after)
    for e in errors:
        print(e)
    if argv[1] == "sync":
        print(f"synced {len(changed)} file(s)" + (": " + ", ".join(changed) if changed else ""))
        return 1 if errors else 0
    for where in changed:
        print(f"{where}: out of date with rules/calls.toml; run python3 scripts/rules.py sync")
    print(f"{len(rules['calls'])} calls; {len(changed)} file(s) out of date; {len(errors)} error(s)")
    return 1 if errors or changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
