# Screening

Metrics 9 and 10 are about the whole practice, not the CoCM caseload:
- **Metric 9:** how many of the patients seen this month have been screened for
  depression in the past year.
- **Metric 10:** how many of this month's first PHQ-9s were positive.

The data comes from the EHR, not the registry.

**Used by:** metrics 9 and 10.

## What NYS says

- Metric 9 numerator: patients who "received a PHQ-2 or 9 either during this visit **or**
  have been screened in the last 12 months."
- Metric 9 denominator: patients "seen in the practice for any reason this month that meet
  practice criteria for universal depression screen (Refer to practice workflow)."
- Metric 10: patients who "scored a 10 or higher on their initial PHQ-9 this month", out
  of patients "who received their initial PHQ-9 during this month."
- Both are all-payer, and "not tracked in your CoCM registry."

([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#9-depression-screening-rate))

## The rule

### Who should be screened (metric 9 denominator)

Count each patient **once**, if this month they had at least one **qualifying visit** and
were **<!--rule:who-should-be-screened.age_floor-->12<!--/rule--> or older** on the visit date. There are no other exclusions. *Our call:
[who should be screened](../../reference/our-calls.md#who-should-be-screened).*

A qualifying visit is an in-person or telehealth visit with a **medical provider**,
billed with one of these codes:

<!--rules:visit-codes-table-->
| Visit | Codes |
|---|---|
| Office or outpatient evaluation and management (E&M) | 99202–99205, 99212–99215 |
| Preventive medicine, new and established | 99381–99397 |
| Medicare annual wellness visit | G0438, G0439 |
| Telehealth equivalents of the above | To be confirmed |
<!--/rules-->

**<!--rule:who-should-be-screened.excluded_codes-->99211<!--/rule--> is left out.** It's an E&M code, but it's normally billed for a nurse-only visit,
and nurse-only visits don't qualify.

These aren't qualifying visits:
- nurse-only, injection, lab and vaccine visits;
- visits with the BHCM, the psychiatric consultant or any behavioral health clinician;
- visits with diabetes educators, nutritionists, care coordinators or community health
  workers;
- phone calls without a billed E&M service, and portal messages.

NYS leaves the criteria to each practice's workflow. The guide sets one standard so that
rates from different practices mean the same thing. A practice whose workflow is
different (for example, adults only) should disclose it.

### What counts as screened (metric 9 numerator)

A patient is screened if they have a **scored PHQ-2 or PHQ-9 dated in the <!--rule:what-counts-as-screened.lookback_months-->12<!--/rule--> months ending
on the last day of the month**. Who gave it and why don't matter. *Our call:
[what counts as screened](../../reference/our-calls.md#what-counts-as-screened).*

- A CoCM patient's monitoring PHQ-9 counts.
- A positive PHQ-2 with no follow-up PHQ-9 still counts as screened. Following up a
  positive screen is good care, but it isn't what metric 9 measures.
- A declined or unscored screen does not count.
- A PHQ-A (the adolescent PHQ-9) counts as a PHQ-9. *Our call:
  [PHQ-A counts as PHQ-9](../../reference/our-calls.md#phq-a-counts-as-phq-9).*

### Initial PHQ-9 (metric 10)

A PHQ-9 is a patient's **initial PHQ-9** if it's dated this month and the patient has
**no other scored PHQ-9 in the <!--rule:initial-phq-9.lookback_days-->365<!--/rule--> days before it**. Each patient counts at most once a
month, on their first PHQ-9 of the month. Who gave it doesn't matter. *Our call:
[initial PHQ-9](../../reference/our-calls.md#initial-phq-9).*

- **Denominator:** patients with an initial PHQ-9 this month.
- **Numerator:** those whose initial PHQ-9 scored 10 or more.

A PHQ-2 is never an initial PHQ-9, even though its two questions are the first two of the
PHQ-9.

### Screening or monitoring?

The archived draft had sites label each PHQ as "screening" or "monitoring", and
excluded monitoring PHQs from metrics 9 and 10. The rules above don't need that label:

- Metric 9 counts any PHQ.
- Metric 10's <!--rule:initial-phq-9.lookback_days-->365<!--/rule-->-day rule excludes a CoCM patient's monthly PHQ-9s on its own, because
  each follows another within a year.

That removes the hardest step in building the report from an EHR.

## Worked example

Reporting month: March 2025.

| Patient | Age | March visits | PHQs on record | Metric 9 | Metric 10 |
|---|---|---|---|---|---|
| A | 45 | Office visit, 99214 | PHQ-2 of 1, 3 Mar | Denominator and **screened** | — (PHQ-2 only) |
| B | 30 | Annual physical, 99395 | PHQ-9 of 14, 12 Mar; no PHQ-9 since 2023 | Denominator and **screened** | **Initial, positive** |
| C | 52 | Office visit, 99213 | PHQ-9 of 8, 20 Jun 2024 | Denominator and **screened** (within 12 months) | — |
| D | 60 | Office visit, 99213; a BHCM session | Monthly CoCM PHQ-9s, most recently 6 Mar | Denominator and **screened** | No: had a PHQ-9 in February |
| E | 38 | Office visit, 99214 | Screen declined, 14 Mar; last PHQ in 2023 | Denominator, **not screened** | — |
| F | 9 | Well-child visit, 99393 | — | Not in denominator: under 12 | — |
| G | 50 | Nurse visit for a flu shot | — | Not in denominator: not a qualifying visit | — |
| H | 16 | Office visit, 99213 | PHQ-A of 7, 18 Mar; none before | Denominator and **screened** | **Initial, negative** |

- Metric 9: 5 of 6 screened (A, B, C, D and H, out of A to E and H), or **83.3%**.
- Metric 10: 1 of 2 positive, or **50.0%**.

## What the program should do

- **Write down the practice's screening workflow** and compare it with the rule above.
  Disclose any differences, such as a different age floor.
- **Record every PHQ-2 and PHQ-9 as a scored, structured result**, including declines,
  so a decline isn't mistaken for a missed screen.
- **Screen at the visit when the last screen is close to a year old**, not only at
  annual physicals. Patients who come in only for acute visits are the usual gap.

## Where the data lives

All of it is in the EHR or practice-management system.

| Fact | Where |
|---|---|
| Visits, codes and provider | Encounters joined to charges or procedures, with the rendering provider's type or specialty |
| Date of birth | Patient demographics |
| PHQ-2 and PHQ-9 results | Questionnaire results, flowsheet rows or observations with a structured total score. Check for more than one questionnaire or flowsheet row per instrument (PCP, BHCM, adolescent, patient portal) |

- **Classify providers by type, not by department.** A behavioral health clinician may
  work in a primary care department.
- **Pull PHQs from every place they're recorded.** Screening rates are often understated
  because one questionnaire version or one department's flowsheet was missed.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting every encounter, including nurse, lab and BHCM visits | Denominator inflated; rate understated |
| Counting visits instead of patients | Denominator inflated for patients seen more than once |
| Including children under 12 | Denominator inflated with patients no standard workflow screens |
| Using age at the run date | Patients who just turned 12 are misclassified |
| Counting a declined screen as screened | Rate overstated |
| Treating every PHQ-9 in the month as initial | Metric 10 dominated by CoCM monitoring scores |
| Missing one of several PHQ questionnaire versions | Rate understated |

## For automation

- [`practice_visit`](../../reference/data-contract.md#t7-practice_visit--the-denominator-for-metric-9)
  holds every visit with provider category and billing codes. The qualifying-visit list,
  including leaving out 99211, is a calculator setting.
- [`scale_result`](../../reference/data-contract.md#t5-scale_result--one-row-per-completed-scored-administration)
  needs <!--rule:what-counts-as-screened.lookback_months-->12<!--/rule--> months of PHQ-2 and PHQ-9 history for metric 9. Metric 10 needs PHQ-9 history
  going back <!--rule:initial-phq-9.lookback_days-->365<!--/rule--> days from the earliest PHQ-9 in the month.
- [`site_month.screening_age_floor`](../../reference/data-contract.md#t8-site_month--one-row-per-submission)
  records the floor used.
- The data contract has no screening-or-monitoring column; rows are selected by instrument and date.
