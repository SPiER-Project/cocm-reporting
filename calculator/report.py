"""A plain-text summary of the calculator's results."""

NAMES = {
    "m1": "Total enrollment",
    "m2": "Medicaid enrollment",
    "m3": "Newly enrolled",
    "m4": "Average duration of treatment",
    "m5": "Monthly contact rate",
    "m6": "Improvement rate",
    "m7": "Remission rate",
    "m8": "Psychiatric consultation rate",
    "m9": "Depression screening rate",
    "m10": "Depression screening yield",
    "m11": "BHCM staffing",
}
NO_VALUE = "no value (nobody to measure)"


def value(m, r):
    if "count" in r:
        return str(r["count"])
    if m == "m4":
        return f"{r['weeks']} weeks" if r["weeks"] is not None else NO_VALUE
    if m == "m11":
        return f"{r['fte']} FTE" if r["fte"] is not None else "not attested"
    if r["percent"] is None:
        return NO_VALUE
    text = f"{r['numerator']} of {r['denominator']}, {r['percent']}%"
    if m == "m10":  # NYS asks for the count and the proportion
        plural = "" if r["numerator"] == 1 else "s"
        return f"{r['numerator']} patient{plural}, {text}"
    return text


def summary(results):
    lines = [f"CoCM caseload metrics for {results['reporting_month']}", ""]
    width = max(len(n) for n in NAMES.values())
    for m, name in NAMES.items():
        lines.append(f"  {m[1:]:>2}. {name:<{width}}  {value(m, results['metrics'][m])}")
    for title, key in (("Disclosures", "disclosures"), ("Warnings", "warnings")):
        if results[key]:
            lines += ["", f"{title}:"] + [f"  - {x}" for x in results[key]]
    if results["fell_out"]:
        lines += ["", "Who fell out of each numerator (keep this at the site):"]
        for m, rows in results["fell_out"].items():
            lines.append(f"  {m[1:]}. {NAMES[m]}")
            lines += [f"     {r['patient_id']}: {r['reason']}" for r in rows]
    return "\n".join(lines)
