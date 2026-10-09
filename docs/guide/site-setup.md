# Site setup

The decisions and fixes a site makes once, before its first report, and revisits only
when its systems or program change. Most monthly reporting problems trace back to one of
these steps being skipped.

Work through them in order. Allow a few weeks: several steps need someone from billing or
IT. At the end, record what was decided in the [setup record](#the-setup-record).

## 1. Name the people

| Role | Does | Usually |
|---|---|---|
| **Owner** | Signs off the submission each month; makes the site's decisions below | The CoCM program lead |
| **Report writer** | Runs the extracts and calculates the metrics | An analyst, a registry administrator, or the program lead in a spreadsheet site |
| **Billing contact** | Supplies coverage and visit data; maintains the payer mapping | Someone from billing or practice management |
| **Clinical reviewer** | Agrees the primary-scale choices and any thresholds marked *needs clinical sign-off* | The psychiatric consultant or medical director |

## 2. Choose your route

Decide where each fact will come from: a spreadsheet registry, a registry product plus an
EHR report, or the EHR alone. [Collecting the data](../collecting/overview.md#pick-your-route)
describes the three. Write down the source system for each row of the
[where each fact lives](../collecting/overview.md#where-each-fact-lives) table.

## 3. Link the registry and the EHR

Every patient in the registry needs their **MRN**, so registry data can be joined to
coverage, visits and screening from the EHR. Check a sample of 20 registry patients
against the EHR. Any patient who can't be matched drops out of every Medicaid metric.
See [one patient id](../collecting/overview.md#one-patient-id).

## 4. Build the payer mapping

List every payer and plan the practice bills, and assign each one a category:

| Plan as it appears in billing | Category | Medicaid? |
|---|---|---|
| *(each plan, as named)* | Medicaid fee-for-service, Medicaid managed care (including HARP), dual, Child Health Plus, Essential Plan, Medicare, commercial, self-pay, other | Yes for the first three |

- **Map by plan, not by carrier.** Many carriers sell Medicaid managed care, Child Health
  Plus, Essential Plan and commercial plans under the same name.
- **Confirm the coverage report shows effective dates**, so status can be taken on the
  first of the month.
- **Keep the mapping as a list the billing contact owns**, and add new plans as they
  appear.

See [Medicaid](concepts/medicaid.md#what-the-program-should-do).

## 5. Fix how enrollment and discharge are recorded

- **Enrollment date is the BHCM's initial assessment.** Check that it isn't the referral
  date or the date the record was created. If past dates are wrong, correct open
  episodes; leave closed ones alone unless the error is large.
- **Every closed episode has a discharge date and reason.** Close any episode that has
  ended but is still open.
- **Apply the inactivity rule.** Find every open episode with no clinical contact in the
  last <!--rule:inactivity-discharge.days-->90<!--/rule--> days, and either re-engage the patient or discharge them. Then make the
  <!--rule:inactivity-discharge.days-->90<!--/rule-->-day review part of the monthly routine.
- **Returning patients get a new episode**, not a reopened one.

If there's no enrollment record at all, the site will infer enrollment from billing and
must disclose it. A structured enrollment record is worth setting up instead. See
[enrollment and discharge](concepts/enrollment-and-discharge.md).

## 6. Set the primary scale

With the clinical reviewer:

- **Confirm which scale the program uses for each condition.** Start from the
  [default mapping](concepts/scales-and-outcomes.md#primary-scale).
- **Choose PHQ-9 or SMFQ for adolescent depression**, and use the same one for every
  adolescent.
- **Record a primary scale on every open episode**, and add the field to the enrollment
  workflow for new ones.
- **Check the registry or EHR can store every scale the program uses**, with a total score
  and date, and with each form (child, caregiver, teacher) kept separate.
- **Agree whether to use the thresholds marked *needs clinical sign-off*** on the
  [instruments](../reference/instruments.md) page for the scales the program uses. Note
  any the site uses differently.

## 7. Decide what counts as a treatment contact

Write down, in one sentence, how the records tell a treatment contact from an outreach
attempt, a scheduling call or a message. For example:
- "a contact marked 'session' in the registry"; or
- "a BHCM encounter with a signed progress note on the same day".

The rule goes in every submission. If the records can't tell them apart, change the
contact log so they can; until then, the contact rate will be overstated. See
[clinical contact](concepts/contacts-and-reviews.md#clinical-contact).

Make sure outreach attempts are logged too, separately from contacts.

## 8. Record case reviews patient by patient

Set up a way for the consultant or BHCM to record, for each patient discussed, the
review date and the recommendation. A registry consultation log, a structured EHR field,
or a tab in the spreadsheet all work. A meeting note listing names doesn't. See
[psychiatric case review](concepts/contacts-and-reviews.md#psychiatric-case-review-metric-8).

## 9. Check the screening workflow

- **Compare the practice's universal screening workflow with the guide's:**
  - patients <!--rule:who-should-be-screened.age_floor-->12<!--/rule--> and older;
  - at qualifying medical visits;
  - PHQ-2 or PHQ-9 at least yearly.
  
  If the practice's workflow differs (for example, adults only), decide whether to change
  it or to report under it and disclose the difference.
- **List every place a PHQ-2, PHQ-9 or PHQ-A is recorded:** each questionnaire, flowsheet
  row and department, including the BHCM's and the patient portal's. The visit and PHQ
  reports must cover all of them.
- **Confirm provider types are recorded** well enough to tell medical visits from nurse,
  lab and behavioral health visits.

See [screening](concepts/screening.md).

## 10. Check dates

Pick five events from late on the last day of a recent month: a scale, a contact, a
visit. Confirm each one's date comes out as that day in the extract, not the next. If
any come out a day late, the source stores UTC timestamps; convert them to local time
before taking the date. See [reporting month](concepts/reporting-month.md).

## 11. Set up BHCM FTE

Start a simple monthly record of each BHCM's CoCM share, with start dates, end dates and
extended leave. See [BHCM FTE](concepts/bhcm-fte.md).

## 12. Do a dry run

Report a recent past month in full before the first real submission.

- **Run the extracts and calculate all eleven metrics**, following each
  [metric page](start-here.md#the-metrics).
- **Read the patient list behind each number**, not just the number. Do the BHCMs
  recognize the enrolled caseload? Are the patients counted as not improved the ones the
  team would expect?
- **Look for the usual problems:**
  - an enrolled count well above the BHCMs' real caseloads;
  - a contact rate near 100%, which often means outreach is being counted;
  - a screening rate far below what the clinic expects, which often means a missed
    questionnaire.
- **Set the monthly calendar:** extracts on or after the <!--rule:when-to-run-the-report.earliest_run_day-->15<!--/rule-->th, review, sign-off, and
  submission before the NYS deadline.

## The setup record

Keep a copy of this table with the site's reporting files, and update it when anything
changes. Its answers are what the site discloses to NYS.

| Decision | Our answer | Decided by | Date |
|---|---|---|---|
| Route, and the source system for each fact | | | |
| Payer mapping location and owner | | | |
| Where enrollment is recorded (registry, EHR record, or billing inferred) | | | |
| Primary scale for each condition; PHQ-9 or SMFQ for adolescents | | | |
| Thresholds used for scales that need clinical sign-off | | | |
| How a treatment contact is identified | | | |
| How case reviews are recorded | | | |
| Screening workflow, and any difference from the guide | | | |
| Every source of PHQ results | | | |
| Monthly run date and sign-off | | | |
