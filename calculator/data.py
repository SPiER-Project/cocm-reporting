"""Reading the eight data-contract tables and the rules file.

Everything here works on text, not paths, so the same code can run in a browser (through
Pyodide) on files the user drops in. The command-line entry point in __main__.py does the
file reading.
"""

import csv
import io
import tomllib
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

TABLES = (
    "patient", "coverage", "cocm_episode", "contact", "scale_result",
    "psych_review", "practice_visit", "site_month",
)

INTS = {"total_score", "vanderbilt_symptom_count", "screening_age_floor"}
BOOLS = {"recommendation_documented", "with_caregiver"}
DECIMALS = {"bhcm_fte"}
LISTS = {"billing_codes"}  # separated by ";"


def _convert(column, value):
    if value == "":
        return None
    if column.endswith("_date"):
        return date.fromisoformat(value)
    if column in INTS:
        return int(value)
    if column in BOOLS:
        if value not in ("true", "false"):
            raise ValueError(f"{column} must be true or false, not {value!r}")
        return value == "true"
    if column in DECIMALS:
        return Decimal(value)
    if column in LISTS:
        return [v.strip() for v in value.split(";") if v.strip()]
    return value


def read_table(name, text):
    """One table's CSV text as a list of dicts with typed values."""
    rows = []
    for n, raw in enumerate(csv.DictReader(io.StringIO(text)), start=2):
        try:
            rows.append({k: _convert(k, v) for k, v in raw.items()})
        except ValueError as e:
            raise ValueError(f"{name}.csv line {n}: {e}") from None
    return rows


def read_tables(texts):
    """{table: csv text} to {table: rows}. A missing table is treated as empty."""
    unknown = set(texts) - set(TABLES)
    if unknown:
        raise ValueError(f"not data-contract tables: {', '.join(sorted(unknown))}")
    return {t: read_table(t, texts[t]) if t in texts else [] for t in TABLES}


# Rows that are the same fact from two sources (say a registry and an EHR) are kept once.
SAME_FACT = {
    "patient": ("patient_id",),
    "scale_result": ("patient_id", "administered_date", "instrument", "total_score"),
}


def combine(*sources):
    """Merge several {table: csv text} into one, keeping each fact once.

    A patient is kept once by id (the first source with a birth date wins). A scale result
    is kept once by patient, date, instrument and score, since a registry and an EHR often
    hold the same PHQ-9. Other tables keep every distinct row.
    """
    merged = {}
    for table in TABLES:
        texts = [s[table] for s in sources if s.get(table)]
        if not texts:
            continue
        header, rows, seen = [], [], {}
        for text in texts:
            reader = csv.DictReader(io.StringIO(text))
            for col in reader.fieldnames or []:
                if col not in header:
                    header.append(col)
            for row in reader:
                fields = SAME_FACT.get(table)
                key = tuple(row.get(f, "") for f in fields) if fields else tuple(sorted(row.items()))
                if key in seen:
                    kept = rows[seen[key]]
                    for col, value in row.items():  # fill gaps from the later source
                        if value and not kept.get(col):
                            kept[col] = value
                    continue
                seen[key] = len(rows)
                rows.append(row)
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=header, lineterminator="\n", restval="")
        writer.writeheader()
        writer.writerows(rows)
        merged[table] = out.getvalue()
    return merged


# ------------------------------------------------------------------------- settings


@dataclass
class Settings:
    """The values the calculator takes from rules/calls.toml."""

    decimal_places: int
    time_zone: str
    earliest_run_day: int
    inactivity_days: int
    seventy_days: int
    baseline_window_days: int
    medicaid_categories: set
    counted_contact_kinds: set
    elevated: dict          # threshold key -> at_or_above (missing: not set)
    remission: dict         # threshold key -> {"below": n} or {"symptom_count_below": n}
    improvement: dict       # threshold key -> NYS Appendix A criteria
    boundary_counts: bool
    review_window_days: int
    age_floor: int
    visit_codes: set        # individual qualifying codes
    excluded_codes: set
    screening_lookback_months: int
    initial_lookback_days: int
    phq_a_counts_as: str
    yield_positive_at_or_above: int
    calls: dict = field(default_factory=dict)  # slug -> {title, status, approval}


def _expand(codes):
    out = set()
    for c in codes:
        if "-" in c:
            lo, hi = c.split("-")
            out.update(str(n) for n in range(int(lo), int(hi) + 1))
        else:
            out.add(c)
    return out


def read_rules(text):
    r = tomllib.loads(text)
    c = r["calls"]
    elevated = {k: v["at_or_above"] for k, v in c["elevated-baseline"]["thresholds"].items()
                if "at_or_above" in v}
    remission = {k: {kk: vv for kk, vv in v.items() if kk != "firmness"}
                 for k, v in c["remission-thresholds"]["thresholds"].items()}
    codes = set()
    for v in c["who-should-be-screened"]["visit_types"]:
        codes |= _expand(v["codes"])
    return Settings(
        decimal_places=c["rounding"]["decimal_places"],
        time_zone=c["reporting-month"]["time_zone"],
        earliest_run_day=c["when-to-run-the-report"]["earliest_run_day"],
        inactivity_days=c["inactivity-discharge"]["days"],
        seventy_days=c["seventy-days"]["days"],
        baseline_window_days=c["baseline"]["window_days"],
        medicaid_categories=set(c["who-counts-as-medicaid"]["medicaid_payer_categories"]),
        counted_contact_kinds=set(c["clinical-contact"]["counted_contact_kinds"]),
        elevated=elevated,
        remission=remission,
        improvement=r["nys"]["improvement"],
        boundary_counts=c["fifty-percent-improved"]["boundary_counts"],
        review_window_days=c["psychiatric-case-review"]["window_days"],
        age_floor=c["who-should-be-screened"]["age_floor"],
        visit_codes=codes - set(c["who-should-be-screened"]["excluded_codes"]),
        excluded_codes=set(c["who-should-be-screened"]["excluded_codes"]),
        screening_lookback_months=c["what-counts-as-screened"]["lookback_months"],
        initial_lookback_days=c["initial-phq-9"]["lookback_days"],
        phq_a_counts_as=c["phq-a-counts-as-phq-9"]["counts_as"],
        yield_positive_at_or_above=r["nys"]["screening_yield_positive_at_or_above"],
        calls={k: {"title": v["title"], "status": v["status"], "approval": v["approval"]}
               for k, v in c.items()},
    )
