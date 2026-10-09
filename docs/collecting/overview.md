# Collecting the data

The [guide](../guide/start-here.md) says what each metric counts. This page says where
those facts live in a clinic's systems, which route to take to get them out, and what
every route has to get right.

## Where each fact lives

Almost every site has **at least two sources**:
- the CoCM registry, or whatever stands in for one;
- the EHR or practice-management system.

NYS says as much: metrics 9 and 10 are "not tracked in your CoCM registry." Medicaid
status usually isn't in the registry either, so every Medicaid metric needs both
sources.

| Fact | Usual source | Needed for | Guide page |
|---|---|---|---|
| Enrollment and discharge | **Registry**; otherwise an EHR program-enrollment record; as a last resort, CoCM billing (disclosed) | Metrics 1–8 | [Enrollment and discharge](../guide/concepts/enrollment-and-discharge.md#where-the-data-lives) |
| Coverage, with dates | **Practice management or billing** | Metrics 2–8 | [Medicaid](../guide/concepts/medicaid.md#where-the-data-lives) |
| Clinical contacts and outreach | **Registry** contact log; otherwise BHCM encounters in the EHR | Metric 5, inactivity discharge | [Contacts and reviews](../guide/concepts/contacts-and-reviews.md#where-the-data-lives) |
| Symptom scales on the caseload | **Registry**; otherwise EHR questionnaires or flowsheets | Metrics 5–8 | [Scales and outcomes](../guide/concepts/scales-and-outcomes.md#where-the-data-lives) |
| Primary diagnosis and primary scale | **Registry**; otherwise the diagnosis on the CoCM episode | Metrics 6–8 | [Scales and outcomes](../guide/concepts/scales-and-outcomes.md#primary-scale) |
| Psychiatric case reviews | **Registry**; otherwise consultant notes, often unstructured | Metric 8 | [Contacts and reviews](../guide/concepts/contacts-and-reviews.md#psychiatric-case-review-metric-8) |
| Practice visits with codes and provider type | **EHR or practice management** | Metric 9 | [Screening](../guide/concepts/screening.md#where-the-data-lives) |
| PHQ-2 and PHQ-9 across the practice | **EHR**, every questionnaire and flowsheet that holds one | Metrics 9–10 | [Screening](../guide/concepts/screening.md#where-the-data-lives) |
| Date of birth | **EHR or practice management** | Metric 9 | — |
| BHCM FTE | **The program lead**, attested | Metric 11 | [BHCM FTE](../guide/concepts/bhcm-fte.md#where-the-data-lives) |

## Pick your route

All three routes produce the same facts. Most sites end up mixing them: the registry
for the CoCM facts, and the EHR for everything else.

### 1. A spreadsheet registry

**For:** sites whose CoCM registry is a spreadsheet, and sites without a report writer.

Fill in the reporting workbook from the registry spreadsheet and one or two standard
reports the practice-management system can already run (visits, PHQs, coverage). The
calculator page reads the workbook directly. See [the workbook route](workbook.md).

- **Cost:** some manual work each month, mostly the visit and screening data for metric 9.
- **Risk:** hand-copied dates and missing rows. Keep the copying to a minimum and check
  counts against the source.

### 2. A registry product plus an EHR report

**For:** sites with a dedicated CoCM registry, whether a commercial
measurement-based-care platform, a registry the site built, or one built into the EHR.

Export the CoCM facts from the registry, and the coverage, visits and practice-wide PHQs
from the EHR. A registry mapping says which registry field supplies each fact, and
where the registry falls short.

- Mappings so far: [a prototype CoCM registry](registries/prototype-cocm-registry.md).
- **Watch for:**
  - contact logs that record only whether the patient was reached, not whether treatment
    was delivered;
  - episodes closed without an end date;
  - scales the registry doesn't support.

### 3. EHR only

**For:** sites that track CoCM in the EHR itself, with no separate registry.

Everything comes from EHR reports, written by the site's report writer from
[what every EHR report must produce](ehrs/README.md).

- **Hardest facts:**
  - **Enrollment:** a structured program-enrollment record, if the EHR has one; otherwise
    billing, disclosed.
  - **Which contacts delivered treatment:** encounter types and signed notes.
  - **The primary scale:** usually the default mapping, disclosed.
  - **Case reviews:** often only in consultant notes.
- **FHIR:** a site with access to its EHR's FHIR API can pull patients, coverage,
  encounters and PHQ results that way instead of writing reports. FHIR doesn't help with
  the CoCM-specific facts (enrollment, contact purpose, case reviews), because EHRs don't
  expose them in a standard form.

## What every route must get right

### One patient id

The registry and the EHR have to identify the same patient the same way, or the two
halves never join. Use the **MRN** as the link inside the site. Don't use a registry's
internal id, which the EHR never sees.

The [data contract](../reference/data-contract.md) goes one step further for anything that leaves
the site's systems: it replaces the MRN with a keyed hash, a pseudonym made with a secret
only the site holds. How sites will do that consistently is still open (Q-T3 in
[open questions](../open-questions.md#the-tooling)).

### Event dates in local time

Every date must be when the event happened, in local time. Use the date of service,
administration or review, not the date of the note, the charge, or the record. Convert
UTC timestamps before taking the date. See [reporting month](../guide/concepts/reporting-month.md).

### How far back to extract

A month's report needs more than a month of data:

| Data | Extract from |
|---|---|
| Episodes | Every episode that overlaps the month |
| Contacts and scales for the caseload | Each open episode's enrollment date. The baseline and the inactivity rule both need the full episode |
| Case reviews | <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days before month end |
| Coverage | Every coverage period that overlaps the month |
| Practice visits | The month |
| PHQ-2, PHQ-9 and PHQ-A across the practice | <!--rule:extraction.phq_history_months-->13<!--/rule--> months: <!--rule:what-counts-as-screened.lookback_months-->12<!--/rule--> for metric 9, and <!--rule:initial-phq-9.lookback_days-->365<!--/rule--> days before each PHQ-9 for metric 10 |

### What to disclose

When a site fills a gap with a substitute, it says so in its submission:

- enrollment inferred from billing;
- a primary scale taken from the default mapping, not recorded;
- the rule used to decide which contacts delivered treatment;
- contacts with no recorded author, counted as the BHCM's;
- a screening workflow that differs from the guide's (for example, adults only).

## The monthly routine

| When | What |
|---|---|
| During the month | Document contacts, scales and case reviews as they happen; log outreach attempts |
| Last week of the month | Review the caseload for anyone near <!--rule:inactivity-discharge.days-->90<!--/rule--> days without a clinical contact |
| Month end to the <!--rule:when-to-run-the-report.earliest_run_day-->15<!--/rule-->th | Late notes and charges close. Don't run the report yet |
| On or after the <!--rule:when-to-run-the-report.earliest_run_day-->15<!--/rule-->th | Run the extracts; calculate the metrics; review the patients who fell out of each numerator |
| Before the NYS deadline | Submit the eleven numbers and the disclosures |
