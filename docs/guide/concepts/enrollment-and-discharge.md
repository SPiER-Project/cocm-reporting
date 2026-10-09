# Enrollment and discharge

Who is enrolled in CoCM, from when, and until when. Every CoCM metric starts here: get
enrollment wrong and metrics 1 to 8 are all wrong in the same direction.

**Used by:** metrics 1 to 8.

## What NYS says

- Metrics 1 and 2: patients "enrolled in CoCM this month".
- Metric 3: patients "diagnosed and enrolled in CoCM this month".
- Metric 4: weeks "between initial assessment to date of discharge", for patients
  discharged this month.
- Metrics 6 and 8: patients "enrolled in CoCM for 70 days or greater"; Appendix A says
  "at least 10 weeks".

NYS doesn't define enrollment, enrollment date or discharge.
([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md))

## The rule

### Enrolled

A patient is enrolled from a **documented CoCM enrollment** until they are discharged.
The record can be a registry enrollment or a structured program-enrollment record in the
EHR. *Our call: [what counts as enrolled](../../reference/our-calls.md#what-counts-as-enrolled).*

- A referral is not an enrollment. Neither is a warm handoff or verbal consent with
  nothing recorded.
- A site with no enrollment record at all may infer enrollment from CoCM billing (99492,
  99493, 99494, G2214), and must say so in its submission. Billing undercounts: an
  enrolled patient can go a month without a billable service.

### Enrollment date

The enrollment date is **the date of the BHCM's initial assessment**. If the assessment
takes more than one contact, use the first contact at which a symptom-monitoring scale
was given. This one date is the start for every metric. *Our call:
[enrollment date](../../reference/our-calls.md#enrollment-date).*

### Discharge

A patient is discharged on the date their CoCM episode is closed, for any reason:
graduation, transfer to specialty care, withdrawal, loss to follow-up, death.

A patient with **no clinical contact for 90 consecutive days** is discharged, with a
discharge date of the last clinical contact plus 90 days. *Our call:
[inactivity discharge](../../reference/our-calls.md#inactivity-discharge).*

Don't backdate a discharge to the last contact. Months already reported counted the
patient as enrolled; a backdated discharge changes them after the fact.

A re-enrollment after discharge is a **new episode**, with a new enrollment date and a
new baseline.

### Enrolled this month

A patient is enrolled this month if their enrollment **overlaps the month by at least one
day**: enrollment date on or before the last day, and no discharge before the first day.
A patient discharged on the 1st counts; a patient enrolled on the 31st counts. *Our call:
[enrolled this month](../../reference/our-calls.md#enrolled-this-month).*

### Seventy days

A patient has been enrolled "70 days or greater" when **at least 70 days have elapsed**
between the enrollment date and the last day of the month. If they were discharged during
the month, measure to the discharge date instead. A patient enrolled on 6 January 2025
reaches 70 days on 17 March 2025. *Our call:
[seventy days](../../reference/our-calls.md#seventy-days).*

### Newly enrolled (metric 3)

A patient is newly enrolled if their **enrollment date is in the month**. Enrollment
already requires a qualifying diagnosis, so "diagnosed" adds no separate test. *Our call:
[diagnosed and enrolled](../../reference/our-calls.md#diagnosed-and-enrolled).*

### Duration in weeks (metric 4)

For each patient discharged in the month, count the days from enrollment date to
discharge date. **Average the days, divide by 7, and round to one decimal place.** *Our
call: [duration in weeks](../../reference/our-calls.md#duration-in-weeks).*

## Worked example

Reporting month: March 2025. Assume every patient is a Medicaid patient.

| Patient | Enrolled | Discharged | Enrolled this month? | Days at month end or discharge | 70+ days? | New? | In metric 4? |
|---|---|---|---|---|---|---|---|
| A | 4 Nov 2024 | — | Yes | 147 | Yes | No | No |
| B | 12 Mar 2025 | — | Yes | 19 | No | Yes | No |
| C | 6 Jan 2025 | 20 Mar 2025, graduated | Yes | 73 | Yes | No | Yes, 73 days |
| D | 1 Oct 2024 | 10 Mar 2025, inactivity (last contact 10 Dec) | Yes | 160 | Yes | No | Yes, 160 days |
| E | Referred 25 Mar; assessment booked for April | — | No: not yet enrolled | — | — | — | — |
| F | 2 Sep 2024 | 27 Feb 2025 | No: discharged before March | — | — | — | — |

- Metric 1 and metric 2: 4 (A, B, C, D).
- Metric 3: 1 (B).
- Metric 4: (73 + 160) ÷ 2 = 116.5 days, ÷ 7 = **16.6 weeks**.

Patient D shows two consequences of the inactivity rule:
- D counts as enrolled in March, with no contact, so D lowers March's
  [contact rate](../metrics/05-monthly-contact-rate.md).
- D's 90 inactive days lengthen average duration.

Both are accurate: the patient was on the caseload and wasn't being reached. The fix is
operational, not a reporting one: discharge disengaged patients sooner than 90 days where
the program's protocol allows.

## What the program should do

- Record the enrollment at the initial assessment, with that date, not when the referral
  arrives.
- Close episodes when they end, with a discharge date and reason. An open episode with no
  activity is the most common reason enrollment is overstated.
- Review the caseload monthly for anyone approaching 90 days without a clinical contact,
  and either re-engage them or discharge them.
- Open a new episode for a returning patient rather than reopening the old one.

## Where the data lives

| Fact | Registry | EHR without a registry | Last resort |
|---|---|---|---|
| Enrollment | Enrollment or episode record | Program-enrollment or care-episode record, if the EHR has one | First CoCM billing code (disclosed) |
| Enrollment date | Episode start date, if it records the assessment date | Date of the first BHCM encounter in the episode | Date of first CoCM charge (disclosed; usually late) |
| Discharge date | Episode end date | Episode or program end date | None. Billing can't show a discharge, so apply the inactivity rule |
| Discharge reason | Discharge reason, often free text | Episode end reason | — |

Things to check in a registry:
- An episode status of "planned", "waitlist" or "referred" is not an enrollment.
- An episode can be closed without an end date. Don't fill the gap from the date the
  record was last updated; that's a documentation date.
- A cancelled episode may have been a cancelled referral (never enrolled) or a
  discharge. Only the history shows which.

The [prototype registry mapping](../../mappings/prototype-cocm-registry.md#episode-status)
works through each of these.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting from the referral date | Enrollment overstated; duration understated; patients reach 70 days early |
| Counting only patients billed this month | Enrollment understated |
| Never discharging disengaged patients | Enrollment overstated; contact rate understated |
| Backdating a discharge to the last contact | Prior months change after submission |
| Counting enrollment as of the last day of the month only | Patients discharged mid-month drop out of metrics 5 and 7 |
| Measuring time in treatment to the run date instead of month end | Patients reach 70 days early |
| Reopening an old episode for a returning patient | The old baseline is reused; improvement is measured against the wrong starting point |

## For automation

- [`cocm_episode`](../../data-contract.md#t3-cocm_episode--one-row-per-enrollment) holds
  enrollment and discharge as recorded. "Enrolled this month", days in treatment, newly
  enrolled and duration are derived by the calculator, never extracted.
- `enrollment_source = billing_inferred` triggers the disclosure.
- The inactivity rule can be applied by the calculator from
  [`contact`](../../data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient)
  rows. That only works if the extract includes enough contact history to see 90 days
  back.
