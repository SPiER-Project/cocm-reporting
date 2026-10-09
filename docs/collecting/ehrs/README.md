# EHR reports

What a site's report writer has to produce from the EHR, whatever the EHR. One recipe
per EHR product will follow as they're written. Until then, this page is the
specification any EHR's reports should meet.

Sites with a registry need only the first four reports; EHR-only sites need all eight.
The columns match the [data contract](../../reference/data-contract.md), so the same output can
feed the calculator once it exists.

## Reports every site needs

| Report | One row per | Columns | Rules |
|---|---|---|---|
| Patients | Patient in any other report | Patient id, date of birth | [One patient id](../overview.md#one-patient-id) |
| Coverage | Coverage period overlapping the month | Patient id, payer category, plan name, start date, end date | Every period, not just the current one. [Medicaid](../../guide/concepts/medicaid.md) |
| Practice visits | Visit in the month | Patient id, visit date, provider category, billing codes, modality | Every visit, all payers; the calculator applies the qualifying-visit rule. [Screening](../../guide/concepts/screening.md#who-should-be-screened-metric-9-denominator) |
| PHQ results | Scored PHQ-2, PHQ-9 or PHQ-A in the last <!--rule:extraction.phq_history_months-->13<!--/rule--> months | Patient id, date administered, instrument, total score | Every questionnaire, flowsheet row and observation that holds one, from every department. [Screening](../../guide/concepts/screening.md#what-counts-as-screened-metric-9-numerator) |

## Reports for sites with no registry

| Report | One row per | Columns | Rules |
|---|---|---|---|
| CoCM episodes | Episode overlapping the month | Patient id, enrollment date, enrollment source, primary condition, primary scale, discharge date, discharge reason | From a program-enrollment record if the EHR has one; otherwise inferred from billing and disclosed. [Enrollment and discharge](../../guide/concepts/enrollment-and-discharge.md) |
| Contacts | BHCM or CoCM-team encounter since each episode began | Patient id, date, staff role, kind (treatment, outreach attempt, scheduling, no-show, message), modality | Encounter type alone rarely shows treatment; require a signed note. [Contacts and reviews](../../guide/concepts/contacts-and-reviews.md#clinical-contact) |
| Monitoring scales | Scored NYS scale since each episode began | Patient id, date, instrument and form, total score | All seven NYS scales and each form separately. [Scales and outcomes](../../guide/concepts/scales-and-outcomes.md#a-scale-result) |
| Case reviews | Patient reviewed by the consultant in the last <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days | Patient id, review date, recommendation documented | One row per patient, never per meeting. [Contacts and reviews](../../guide/concepts/contacts-and-reviews.md#psychiatric-case-review-metric-8) |

## What a recipe for a specific EHR adds

For each report above:
- which tables, reports or extracts supply it;
- which encounter types, departments, questionnaire and flowsheet IDs, and provider
  types to include;
- the traps particular to that EHR.

No recipes yet. Which EHRs to write them for first depends on which ones NYS's CoCM
sites use most ([tooling plan](../../tooling.md)).
