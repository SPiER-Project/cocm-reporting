"""Reading FHIR R4 resources into the data-contract tables.

    read_fhir(texts, settings, patient_identifier_system=None) -> (tables, notes)

texts is a list of file contents: FHIR Bundles, single resources, JSON arrays of
resources, or NDJSON as written by a FHIR Bulk Data export. tables is {table: csv text},
the same shape the calculator reads from CSV files or the workbook; notes are things the
site should know, such as payer codes it couldn't classify.

Scope: the EHR half of the data, which EHRs expose in standard FHIR.

    Patient       -> patient
    Coverage      -> coverage
    Encounter     -> practice_visit   (billing codes from Encounter.type, or from a Claim)
    Observation   -> scale_result     (the scales with a LOINC total; see instruments.md)

The CoCM half (episodes, contacts, case reviews) has no standard FHIR form that EHRs
expose, so it still comes from the registry or the workbook. The two combine with
calculator.data.combine, provided both use the same patient id: by default the FHIR
Patient.id, or the Patient.identifier with the system the site names.

Where each column lives in FHIR is documented in docs/reference/data-contract.md.
"""

import csv
import io
import json
from datetime import datetime, timedelta, timezone

# Observation codes this reader recognizes: the LOINC total-score codes verified on the
# instruments page. Scales without a LOINC total can't be read from FHIR by code.
LOINC = {
    "44261-6": "phq9",
    "89204-2": "phq_a",
    "55758-7": "phq2",
    "70274-6": "gad7",
    "101698-9": "pcl5",
}
LOINC_SYSTEM = "http://loinc.org"
CPT_SYSTEMS = {
    "http://www.ama-assn.org/go/cpt",
    "urn:oid:2.16.840.1.113883.6.12",
    "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets",
    "urn:oid:2.16.840.1.113883.6.285",
}

# Coverage.type: the PHDSC Source of Payment Typology (US Core's Payer Type value set),
# from NAHDO's published code table, version 9.0 (August 2019). Codes are hierarchical,
# so the longest matching prefix decides.
SOPT_SYSTEM = "https://nahdo.org/sopt"
SOPT = [
    ("14", "dual_medicare_medicaid"),  # Dual Eligibility Medicare/Medicaid Organization
    ("1", "medicare"),
    ("21", "medicaid_managed_care"),   # Medicaid (Managed Care)
    ("22", "medicaid_ffs"),            # Medicaid (Non-managed Care Plan)
    ("23", "child_health_plus"),       # Medicaid/SCHIP: New York's CHIP is Child Health Plus
    ("25", "other"),                   # Medicaid - Out of State: not New York State Medicaid
    ("2", "medicaid_ffs"),             # MEDICAID, not otherwise specified
    ("361", "child_health_plus"),      # State SCHIP program
    ("5", "commercial"),               # Private health insurance
    ("6", "commercial"),               # Blue Cross/Blue Shield
    ("81", "self_pay"),
]
# New York programs a payer code can't tell apart, recognized by plan name.
PLAN_NAMES = [
    ("essential plan", "essential_plan"),
    ("child health plus", "child_health_plus"),
]

# Practitioner taxonomy (NUCC) prefixes that make a visit not a medical one.
BEHAVIORAL = ("2084P", "101Y", "103T", "1041", "106H")  # psychiatry, counselors,
NURSING = ("163W", "164W", "164X")                         # psychologists, social workers,
#                                                           behavior analysts; nurses
FINISHED = {"finished", "arrived", "in-progress", "triaged", "onleave", "unknown"}
FINAL = {"final", "amended", "corrected"}

COLUMNS = {
    "patient": ["patient_id", "birth_date"],
    "coverage": ["patient_id", "payer_category", "start_date", "end_date", "plan_name"],
    "practice_visit": ["visit_id", "patient_id", "visit_date", "provider_category",
                       "billing_codes", "modality"],
    "scale_result": ["result_id", "patient_id", "administered_date", "instrument",
                     "total_score", "vanderbilt_symptom_count", "administered_by_role",
                     "loinc"],
}


# Parsing ------------------------------------------------------------------------------


def _resources(text):
    """Every resource in a file: a Bundle, a resource, a JSON array, or NDJSON."""
    text = text.strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        items = data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        items = []
        for n, line in enumerate(text.splitlines(), start=1):
            if line.strip():
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    raise ValueError(f"line {n} isn't JSON") from None
    out = []
    for item in items:
        if not isinstance(item, dict) or "resourceType" not in item:
            raise ValueError("found something that isn't a FHIR resource")
        if item["resourceType"] == "Bundle":
            for entry in item.get("entry", []):
                if "resource" in entry:
                    out.append((entry.get("fullUrl"), entry["resource"]))
        else:
            out.append((None, item))
    return out


def _new_york(moment):
    """A UTC moment in New York time, by the US daylight-saving rule in force since 2007:
    from 2 a.m. on the second Sunday in March to 2 a.m. on the first Sunday in November.
    Used where there's no time-zone database, as in the browser."""
    utc = moment.astimezone(timezone.utc).replace(tzinfo=None)
    year = utc.year
    march = datetime(year, 3, 8)
    start = march + timedelta(days=(6 - march.weekday()) % 7, hours=2 + 5)    # 2 a.m. EST in UTC
    november = datetime(year, 11, 1)
    end = november + timedelta(days=(6 - november.weekday()) % 7, hours=2 + 4)  # 2 a.m. EDT in UTC
    return utc - timedelta(hours=4 if start <= utc < end else 5)


class _Dates:
    """FHIR dates and dateTimes as the site's local date."""

    def __init__(self, time_zone, notes):
        self.notes = notes
        self.new_york = time_zone == "America/New_York"
        try:
            from zoneinfo import ZoneInfo
            self.zone = ZoneInfo(time_zone)
        except Exception:  # no time-zone database, as in the browser
            self.zone = None

    def __call__(self, value):
        if not value:
            return None
        if len(value) <= 10:
            return value if len(value) == 10 else None  # a year or year-month isn't a day
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if moment.tzinfo is not None and self.zone is not None:
            return moment.astimezone(self.zone).date().isoformat()
        if moment.tzinfo is not None and self.new_york:
            return _new_york(moment).date().isoformat()
        if moment.tzinfo is not None:
            self.notes.add("Times were read as given, without converting to local time; "
                           "an event near midnight may land on the wrong day")
        return moment.date().isoformat()


def _codes(concepts):
    for concept in concepts or []:
        for coding in (concept or {}).get("coding", []):
            yield coding.get("system"), coding.get("code"), coding.get("display")


# Reading ------------------------------------------------------------------------------


def read_fhir(texts, settings, patient_identifier_system=None):
    notes = set()
    when = _Dates(settings.time_zone, notes)
    by_url, by_ref = {}, {}
    resources = []
    for text in texts:
        for full_url, r in _resources(text):
            resources.append(r)
            ref = f"{r['resourceType']}/{r.get('id')}"
            by_ref[ref] = r
            if full_url:
                by_url[full_url] = r

    def resolve(reference):
        ref = (reference or {}).get("reference", "")
        return by_url.get(ref) or by_ref.get(ref) or by_ref.get("/".join(ref.split("/")[-2:]))

    # Patients, and the id each one goes by.
    patient_ids = {}
    for r in resources:
        if r["resourceType"] != "Patient":
            continue
        pid = r.get("id")
        if patient_identifier_system:
            pid = next((i.get("value") for i in r.get("identifier", [])
                        if i.get("system") == patient_identifier_system), None)
            if pid is None:
                notes.add(f"Patients without an identifier in {patient_identifier_system} "
                          "were left out")
                continue
        patient_ids[f"Patient/{r.get('id')}"] = pid
        for url, other in by_url.items():
            if other is r:
                patient_ids[url] = pid

    def patient(reference):
        ref = (reference or {}).get("reference", "")
        return patient_ids.get(ref) or patient_ids.get("/".join(ref.split("/")[-2:]))

    rows = {t: [] for t in COLUMNS}
    for r in resources:
        if r["resourceType"] == "Patient" and patient(
                {"reference": f"Patient/{r.get('id')}"}):
            rows["patient"].append([patient({"reference": f"Patient/{r.get('id')}"}),
                                    r.get("birthDate", "")])

    # Coverage -----------------------------------------------------------------------
    unclassified = set()
    for r in (r for r in resources if r["resourceType"] == "Coverage"):
        if r.get("status") in ("cancelled", "entered-in-error"):
            continue
        pid = patient(r.get("beneficiary"))
        if pid is None:
            continue
        plan = next((c.get("name") or c.get("value") for c in r.get("class", [])
                     if any(code == "plan" for _, code, _ in _codes([c.get("type")]))), None)
        payor = next((p.get("display") for p in r.get("payor", []) if p.get("display")), None)
        name = plan or payor or ""
        category = None
        for label, cat in PLAN_NAMES:
            if label in name.lower():
                category = cat
        if category is None:
            for system, code, _ in _codes([r.get("type")]):
                if system in (SOPT_SYSTEM, "urn:oid:2.16.840.1.113883.3.221.5") and code:
                    category = next((cat for prefix, cat in sorted(SOPT, key=lambda x: -len(x[0]))
                                     if code.startswith(prefix)), "other")
                    break
        if category is None:
            category = "other"
            unclassified.add(name or "(no plan name)")
        period = r.get("period", {})
        start = when(period.get("start")) or "1900-01-01"
        rows["coverage"].append([pid, category, start, when(period.get("end")) or "", name])
    if unclassified:
        notes.add("Coverage with no recognized payer type was counted as other: "
                  + ", ".join(sorted(unclassified)))

    # Practice visits --------------------------------------------------------------------
    claim_codes = {}
    for r in (r for r in resources if r["resourceType"] == "Claim"):
        for item in r.get("item", []):
            codes = [code for system, code, _ in _codes([item.get("productOrService")])
                     if system in CPT_SYSTEMS and code]
            for ref in item.get("encounter", []):
                target = resolve(ref)
                if target is not None:
                    claim_codes.setdefault(id(target), []).extend(codes)
    assumed = 0
    for r in (r for r in resources if r["resourceType"] == "Encounter"):
        if r.get("status") not in FINISHED:
            continue
        pid = patient(r.get("subject"))
        day = when(r.get("period", {}).get("start"))
        if pid is None or day is None:
            continue
        codes = [code for system, code, _ in _codes(r.get("type")) if system in CPT_SYSTEMS and code]
        codes += [c for c in claim_codes.get(id(r), []) if c not in codes]
        taxonomy = []
        for participant in r.get("participant", []):
            who = resolve(participant.get("individual"))
            if who is not None and who.get("resourceType") == "PractitionerRole":
                taxonomy += [code or "" for _, code, _ in _codes(who.get("specialty", []) + who.get("code", []))]
        if any(t.startswith(BEHAVIORAL) for t in taxonomy):
            category = "behavioral_health"
        elif taxonomy and all(t.startswith(NURSING) for t in taxonomy):
            category = "nursing_only"
        else:
            category = "primary_care"
            assumed += not taxonomy
        modality = "video" if (r.get("class") or {}).get("code") == "VR" else "in_person"
        rows["practice_visit"].append([r.get("id"), pid, day, category, ";".join(codes), modality])
    if assumed:
        notes.add(f"{assumed} visits had no practitioner role in the export, so they were "
                  "treated as medical visits")

    # Scale results ------------------------------------------------------------------------
    for r in (r for r in resources if r["resourceType"] == "Observation"):
        if r.get("status") not in FINAL:
            continue
        loinc = next((code for system, code, _ in _codes([r.get("code")])
                      if system == LOINC_SYSTEM and code in LOINC), None)
        if loinc is None:
            continue
        pid = patient(r.get("subject"))
        day = when(r.get("effectiveDateTime") or (r.get("effectivePeriod") or {}).get("start"))
        value = r.get("valueInteger")
        if value is None and "valueQuantity" in r:
            value = r["valueQuantity"].get("value")
        if pid is None or day is None or value is None:
            continue
        rows["scale_result"].append([r.get("id"), pid, day, LOINC[loinc], int(value), "", "", loinc])

    tables = {}
    for table, columns in COLUMNS.items():
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows[table])
        tables[table] = out.getvalue()
    return tables, sorted(notes)
