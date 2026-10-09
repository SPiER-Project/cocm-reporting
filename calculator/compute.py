"""The eleven NYS metrics, computed from the eight data-contract tables.

Each step names the call in docs/reference/our-calls.md that it implements, so a change
to a call can be traced to the code. Every value a call sets comes from Settings, which is
read from rules/calls.toml; nothing here hard-codes a window or threshold.
"""

import calendar
from collections import defaultdict
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

# Scale handling ---------------------------------------------------------------------

# The instrument values that are NYS symptom-monitoring scales (metric 5).
NYS_SCALES = {
    "phq9", "gad7", "pcl5", "psc17", "scared_child", "scared_parent",
    "smfq_child", "smfq_parent", "vanderbilt_parent", "vanderbilt_teacher",
}
# Paired forms: a primary scale covers every form of its instrument.
FORMS = {
    "scared_child": ("scared_child", "scared_parent"),
    "scared_parent": ("scared_child", "scared_parent"),
    "smfq_child": ("smfq_child", "smfq_parent"),
    "smfq_parent": ("smfq_child", "smfq_parent"),
    "vanderbilt_parent": ("vanderbilt_parent", "vanderbilt_teacher"),
    "vanderbilt_teacher": ("vanderbilt_parent", "vanderbilt_teacher"),
}
# The key each form's thresholds and improvement criteria are filed under in the rules.
THRESHOLD_KEY = {
    "scared_child": "scared", "scared_parent": "scared",
    "vanderbilt_parent": "vanderbilt", "vanderbilt_teacher": "vanderbilt",
}
PHQ = {"phq2", "phq9"}  # for screening, after the PHQ-A is normalized to phq9


def threshold_key(form):
    return THRESHOLD_KEY.get(form, form)


# Small helpers ------------------------------------------------------------------------


def month_bounds(month):
    year, mon = (int(x) for x in month.split("-"))
    return date(year, mon, 1), date(year, mon, calendar.monthrange(year, mon)[1])


def months_back(first_of_month, n):
    """The first day of the month n months before first_of_month (after it, if n < 0)."""
    index = first_of_month.year * 12 + first_of_month.month - 1 - n
    return date(index // 12, index % 12 + 1, 1)


def rounded(value, places):
    return str(Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def rate(numerator, denominator, places):
    """A percentage, or None when there's no one to measure (empty denominators)."""
    if denominator == 0:
        return None
    return rounded(Decimal(numerator) * 100 / denominator, places)


def age_on(birth, day):
    return day.year - birth.year - ((day.month, day.day) < (birth.month, birth.day))


# The calculation ------------------------------------------------------------------------


def calculate(tables, settings, month):
    s = settings
    first, last = month_bounds(month)

    # Normalize instruments: the PHQ-A counts as a PHQ-9 (phq-a-counts-as-phq-9).
    scores = []
    for r in tables["scale_result"]:
        inst = s.phq_a_counts_as if r["instrument"] == "phq_a" else r["instrument"]
        scores.append({**r, "instrument": inst})
    by_patient = defaultdict(list)
    for r in sorted(scores, key=lambda r: (r["administered_date"], r["result_id"])):
        by_patient[r["patient_id"]].append(r)

    treatment = defaultdict(list)  # clinical contacts only (clinical-contact)
    for c in tables["contact"]:
        if c["contact_kind"] in s.counted_contact_kinds:
            treatment[c["patient_id"]].append(c["contact_date"])
    for dates in treatment.values():
        dates.sort()

    # Medicaid on the first of the month, primary or secondary (who-counts-as-medicaid).
    medicaid = set()
    for c in tables["coverage"]:
        if (c["payer_category"] in s.medicaid_categories and c["start_date"] <= first
                and (c["end_date"] is None or c["end_date"] >= first)):
            medicaid.add(c["patient_id"])

    # Episodes --------------------------------------------------------------------------
    episodes = {}
    for e in tables["cocm_episode"]:
        p, start = e["patient_id"], e["enrollment_date"]
        # Inactivity discharge: the first run of more than N days with no clinical
        # contact, from the enrollment date, closes the episode N days after its start.
        inactive = None
        previous = start
        for d in [d for d in treatment[p] if start <= d <= last] + [None]:
            if d is None or (d - previous).days > s.inactivity_days:
                if previous + timedelta(days=s.inactivity_days) <= last:
                    inactive = previous + timedelta(days=s.inactivity_days)
                break
            previous = d
        recorded = e["discharge_date"]
        ends = [d for d in (recorded, inactive) if d is not None and d <= last]
        discharge = min(ends) if ends else None
        # Enrolled this month: overlaps the month by a day (enrolled-this-month).
        if start <= last and (discharge is None or discharge >= first):
            end = discharge or last
            current = episodes.get(p)
            if current is None or start > current["enrollment_date"]:
                episodes[p] = {**e, "discharge": discharge, "inactive": inactive,
                               "end": end, "days": (end - start).days}

    # Per-patient facts ------------------------------------------------------------------
    patients = {}
    fell_out = defaultdict(list)
    ids = {r["patient_id"] for r in tables["patient"]} | set(episodes)
    for p in sorted(ids):
        facts = {"medicaid": p in medicaid, "enrolled_this_month": p in episodes}
        patients[p] = facts
        if p not in episodes:
            continue
        e = episodes[p]
        start, end = e["enrollment_date"], e["end"]
        facts["days_in_treatment"] = e["days"]
        facts["new_this_month"] = first <= start <= last
        facts["effective_discharge_date"] = e["discharge"].isoformat() if e["discharge"] else None
        facts["discharged_this_month"] = e["discharge"] is not None and first <= e["discharge"] <= last
        seventy = e["days"] >= s.seventy_days

        mine = [r for r in by_patient[p] if start <= r["administered_date"] <= end]

        # Active treatment: a clinical contact and any NYS scale in the month, while
        # enrolled (active-treatment).
        window_start = max(first, start)
        has_contact = any(window_start <= d <= end for d in treatment[p])
        has_scale = any(window_start <= r["administered_date"] and r["instrument"] in NYS_SCALES
                        for r in mine)
        facts["active_treatment"] = has_contact and has_scale
        if not has_contact or not has_scale:
            missing = [w for w, ok in (("clinical contact", has_contact), ("scale", has_scale)) if not ok]
            facts["_m5_reason"] = "no " + " or ".join(missing) + " this month"

        # Primary scale, baseline and outcomes, form by form (primary-scale, baseline,
        # paired-forms, elevated-baseline, current-score-for-improvement, remission-*).
        forms = FORMS.get(e["primary_scale"], (e["primary_scale"],))
        elevated_any, improved_any, remission_any = False, False, False
        notes, remission_notes = [], []
        for form in forms:
            series = [r for r in mine if r["instrument"] == form]
            if not series:
                continue
            in_window = [r for r in series
                         if r["administered_date"] <= start + timedelta(days=s.baseline_window_days)]
            base = (in_window or series)[0]
            key = threshold_key(form)
            b = base["total_score"]
            elevated = key in s.elevated and b >= s.elevated[key]
            if not elevated:
                notes.append(f"{form} baseline {b} isn't elevated")
                continue
            elevated_any = True
            later = series[series.index(base) + 1:]
            # Improvement: the latest score since baseline, carried forward.
            if later:
                cur = later[-1]["total_score"]
                crit = s.improvement.get(key, {})
                ok = False
                if "fraction_of_baseline" in crit:
                    limit = Decimal(str(crit["fraction_of_baseline"])) * b
                    ok = cur <= limit if s.boundary_counts else cur < limit
                if "or_below" in crit:
                    ok = ok or cur < crit["or_below"]
                if "points_better" in crit:
                    ok = ok or b - cur >= crit["points_better"]
                improved_any = improved_any or ok
                if not ok:
                    notes.append(f"{form} is {cur} against a baseline of {b}")
            else:
                notes.append(f"no {form} score since the baseline")
            # Remission: the last score dated this month, below the threshold.
            this_month = [r for r in series if r["administered_date"] >= first]
            rule = s.remission.get(key, {})
            if not this_month:
                remission_notes.append(f"no {form} score this month")
            elif "below" in rule:
                score = this_month[-1]["total_score"]
                remission_any = remission_any or score < rule["below"]
                if score >= rule["below"]:
                    remission_notes.append(f"{form} is {score}; remission is below {rule['below']}")
            elif "symptom_count_below" in rule:
                n = this_month[-1].get("vanderbilt_symptom_count")
                remission_any = remission_any or (n is not None and n < rule["symptom_count_below"])
                remission_notes.append(f"{form} symptom count is {n}")
            else:
                remission_notes.append(f"no remission threshold set for {form}")
        facts["elevated_baseline"] = elevated_any
        facts["improved"] = improved_any if (seventy and elevated_any) else None
        facts["in_remission"] = remission_any
        facts["_outcome_notes"] = notes or [f"no {e['primary_scale']} scores since enrollment"]
        facts["_remission_notes"] = remission_notes or facts["_outcome_notes"]

        # Psychiatric case review in the window ending at month end (psychiatric-case-review).
        window = last - timedelta(days=s.review_window_days - 1)
        reviews = [r["review_date"] for r in tables["psych_review"]
                   if r["patient_id"] == p and r["recommendation_documented"]]
        facts["psych_review_in_window"] = any(window <= d <= last for d in reviews)
        facts["_last_review"] = max(reviews).isoformat() if reviews else None

    # The CoCM metrics -------------------------------------------------------------------
    enrolled = [p for p, f in patients.items() if f["enrolled_this_month"]]
    med = [p for p in enrolled if patients[p]["medicaid"]]
    m6_den = [p for p in med if patients[p]["improved"] is not None]
    m6_num = [p for p in m6_den if patients[p]["improved"]]
    m8_den = [p for p in m6_den if p not in m6_num]
    m8_num = [p for p in m8_den if patients[p]["psych_review_in_window"]]
    m5_num = [p for p in med if patients[p]["active_treatment"]]
    m7_num = [p for p in med if patients[p]["in_remission"]]
    durations = [patients[p]["days_in_treatment"] for p in med if patients[p]["discharged_this_month"]]

    for p in med:
        f = patients[p]
        if not f["active_treatment"]:
            fell_out["m5"].append((p, f["_m5_reason"]))
        if not f["in_remission"]:
            reason = ("no elevated baseline" if not f["elevated_baseline"]
                      else "; ".join(f["_remission_notes"]))
            fell_out["m7"].append((p, reason))
    for p in m6_den:
        if p not in m6_num:
            fell_out["m6"].append((p, "; ".join(patients[p]["_outcome_notes"])))
    for p in m8_den:
        if p not in m8_num:
            last_review = patients[p]["_last_review"]
            fell_out["m8"].append((p, f"last review {last_review}, outside the window"
                                   if last_review else "no psychiatric case review"))

    metrics = {
        "m1": {"count": len(enrolled)},
        "m2": {"count": len(med)},
        "m3": {"count": sum(patients[p]["new_this_month"] for p in med)},
        "m4": {"discharged_days": durations,
               "weeks": rounded(Decimal(sum(durations)) / len(durations) / 7, s.decimal_places)
               if durations else None},
        "m5": {"numerator": len(m5_num), "denominator": len(med)},
        "m6": {"numerator": len(m6_num), "denominator": len(m6_den)},
        "m7": {"numerator": len(m7_num), "denominator": len(med)},
        "m8": {"numerator": len(m8_num), "denominator": len(m8_den)},
    }

    # Screening (who-should-be-screened, what-counts-as-screened, initial-phq-9) ----------
    site = tables["site_month"][0] if tables["site_month"] else {}
    floor = site.get("screening_age_floor") or s.age_floor
    born = {r["patient_id"]: r["birth_date"] for r in tables["patient"] if r.get("birth_date")}
    denominator = set()
    for v in tables["practice_visit"]:
        if (first <= v["visit_date"] <= last
                and v["provider_category"] in ("primary_care", "other_medical")
                and set(v["billing_codes"] or []) & s.visit_codes
                and v["patient_id"] in born and age_on(born[v["patient_id"]], v["visit_date"]) >= floor):
            denominator.add(v["patient_id"])
    since = months_back(first, s.screening_lookback_months - 1)
    screened = set()
    for p in denominator:
        if any(r["instrument"] in PHQ and since <= r["administered_date"] <= last
               for r in by_patient[p]):
            screened.add(p)
        else:
            fell_out["m9"].append((p, f"no PHQ-2 or PHQ-9 since {since.isoformat()}"))
    initial, positive = set(), set()
    for p, rows in by_patient.items():
        phq9 = [r for r in rows if r["instrument"] == "phq9"]
        firsts = [r for r in phq9 if first <= r["administered_date"] <= last]
        if not firsts:
            continue
        d = firsts[0]["administered_date"]
        earlier = any(d - timedelta(days=s.initial_lookback_days) <= r["administered_date"] < d
                      for r in phq9)
        if p in patients:
            patients[p]["initial_phq9"] = not earlier
        if not earlier:
            initial.add(p)
            if firsts[0]["total_score"] >= s.yield_positive_at_or_above:
                positive.add(p)
            if p in patients:
                patients[p]["initial_phq9_positive"] = p in positive
    for p in patients:
        patients[p]["in_screening_denominator"] = p in denominator
        if p in denominator:
            patients[p]["screened"] = p in screened
    metrics["m9"] = {"numerator": len(screened), "denominator": len(denominator)}
    metrics["m10"] = {"numerator": len(positive), "denominator": len(initial)}
    metrics["m11"] = {"fte": str(site["bhcm_fte"]) if site.get("bhcm_fte") is not None else None}

    for m in ("m5", "m6", "m7", "m8", "m9", "m10"):
        metrics[m]["percent"] = rate(metrics[m]["numerator"], metrics[m]["denominator"],
                                     s.decimal_places)

    # Disclosures and warnings ---------------------------------------------------------------
    disclosures, warnings = [], []
    sources = sorted({e["enrollment_source"] for e in tables["cocm_episode"]})
    if sources:
        disclosures.append(f"Enrollment sources: {', '.join(sources)}")
    in_month = [episodes[p] for p in enrolled]
    defaulted = [e for e in in_month if e.get("primary_scale_source") == "default_mapping"]
    if defaulted:
        disclosures.append(f"{len(defaulted)} of {len(in_month)} episodes use the default primary-scale mapping")
    unknown = [c for c in tables["contact"] if c["staff_role"] == "unknown"]
    if unknown:
        disclosures.append(f"{len(unknown)} of {len(tables['contact'])} contacts have no recorded author")
    if site.get("treatment_contact_rule"):
        disclosures.append(f"Treatment contacts identified by: {site['treatment_contact_rule']}")
    if floor != s.age_floor:
        disclosures.append(f"Screening age floor {floor}, not the guide's {s.age_floor}")
    run = site.get("extract_run_date")
    earliest = months_back(first, -1) + timedelta(days=s.earliest_run_day - 1)
    if run and run < earliest:
        warnings.append(f"Extract run on {run.isoformat()}, before {earliest.isoformat()}; "
                        "late documentation may be missing")
    unapproved = [k for k, v in s.calls.items() if v["approval"] == "needed"]
    if unapproved:
        warnings.append(f"Provisional: {len(unapproved)} of {len(s.calls)} calls these results "
                        "follow still need approval")

    return {
        "reporting_month": month,
        "metrics": metrics,
        "patients": {p: {k: v for k, v in f.items() if not k.startswith("_")}
                     for p, f in patients.items()},
        "fell_out": {m: [{"patient_id": p, "reason": r} for p, r in sorted(v)]
                     for m, v in sorted(fell_out.items())},
        "disclosures": disclosures,
        "warnings": warnings,
    }
