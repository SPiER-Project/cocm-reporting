# The workbook route

For sites whose CoCM registry is a spreadsheet, or that have no report writer. The site
keeps its registry spreadsheet, adds the few columns the metrics need, and pastes in two
or three standard reports from the practice-management system each month.

**Status:** a template workbook is planned but not built. Until it exists, this page is
a checklist for adapting the spreadsheet a site already has. The site then counts each
metric by hand, following its [metric page](../guide/start-here.md#the-metrics).

## What the registry spreadsheet needs

Most CoCM registry spreadsheets already have a row per patient and a column per month
for contacts and scores. Check for each of these, and add what's missing.

| Needed | Why | Often missing? |
|---|---|---|
| Enrollment date: the date of the initial assessment | Every metric's start date | Sometimes the referral date instead |
| Discharge date and reason | Enrollment and metric 4 | Often blank for patients who drifted away |
| Primary diagnosis and **primary scale** | Metrics 6–8 | Primary scale usually missing |
| Baseline score on the primary scale, with its date | Metrics 6–8 | Usually present |
| Each month's scores, with dates | Metrics 5–7 | Dates often missing; a score in the "March" column isn't enough near month end |
| Each clinical contact, with date and whether treatment was delivered | Metric 5 and inactivity discharge | Often a single "contacted this month" tick, with no way to tell a session from a reminder call |
| Outreach attempts | Inactivity discharge | Often not recorded |
| Each psychiatric case review, with date and whether a recommendation was documented | Metric 8 | Often a single "reviewed" tick |
| MRN | Joining to the EHR reports | Usually present |

**One row per episode, not per patient.** A returning patient gets a new row, with a new
enrollment date and baseline.

**Contacts and reviews in their own tabs.** A tab with one row per contact (date,
patient, type, treatment delivered yes or no) and one with one row per review (date,
patient, recommendation yes or no) works better than monthly tick columns. They keep the
dates, and they're quicker to fill in.

## The reports to paste in each month

From the practice-management or EHR system, as standard reports where they exist:

1. **Coverage on the first of the month** for every patient in the registry: MRN, payer,
   plan, and effective dates. Map each plan to Medicaid or not using the site's
   [payer mapping](../guide/concepts/medicaid.md#what-the-program-should-do).
2. **Visits this month**: MRN, date of birth, visit date, provider type, and billing
   codes. This is the hardest report and the one most worth asking a vendor or billing
   service to set up once.
3. **PHQ-2 and PHQ-9 results** for the past 13 months: MRN, date, instrument, score.

## Checks before submitting

- Does the number of enrolled patients match the caseload the BHCMs think they have?
- Does every patient enrolled 70 days or more have a primary scale and a baseline?
- Is anyone enrolled with no clinical contact in the last 90 days? They should be
  re-engaged or discharged.
- Does every Medicaid managed care plan in the coverage report appear in the payer
  mapping?
