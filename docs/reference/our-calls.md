# Our calls

Every place this guide interprets the [NYS document](nys-source/nys-omh-cocm-metrics-2025.md)
or goes beyond it. The guide's pages state these rules inline; this page collects them,
with the reasoning, in one place.

**Firmness**

- **NYS says**: the source document settles it; we only restate it.
- **Our call**: NYS is silent or ambiguous, so we decided. A site that follows the guide
  should follow the call, and disclose it if NYS asks.
- **Needs clinical sign-off**: our call, but a clinical judgement a reporting team
  shouldn't make alone. Treat the value as provisional.

**Status**

- **Proposed**: drafted, not yet agreed by the project.
- **Adopted**: agreed by the project.
- **Confirmed by NYS**: NYS has given the same answer.

Every call below is **Proposed**. Each lists what it replaces in the archived
[draft v0.1](../archive/reporting-spec-draft-v0.1.md) and
[review notes](../archive/review-notes-v0.1.md), so its history can be traced.

## Summary

| Call | Firmness | Status |
|---|---|---|
| **Reporting** | | |
| [Reporting month](#reporting-month) | Our call | Proposed |
| [When to run the report](#when-to-run-the-report) | Our call | Proposed |
| [Rounding](#rounding) | Our call | Proposed |
| [Empty denominators](#empty-denominators) | Our call | Proposed |
| **Enrollment and discharge** | | |
| [What counts as enrolled](#what-counts-as-enrolled) | Our call | Proposed |
| [Enrollment date](#enrollment-date) | Our call | Proposed |
| [Enrolled this month](#enrolled-this-month) | Our call | Proposed |
| [Inactivity discharge](#inactivity-discharge) | Our call | Proposed |
| [Seventy days](#seventy-days) | Our call | Proposed |
| [Diagnosed and enrolled](#diagnosed-and-enrolled) | Our call | Proposed |
| [Duration in weeks](#duration-in-weeks) | Our call | Proposed |
| **Medicaid** | | |
| [Who counts as Medicaid](#who-counts-as-medicaid) | Our call | Proposed |
| [Remission is a Medicaid metric](#remission-is-a-medicaid-metric) | Our call | Proposed |
| **Scales and outcomes** | | |
| [Primary scale](#primary-scale) | Our call | Proposed |
| [Baseline](#baseline) | Our call | Proposed |
| [Elevated baseline](#elevated-baseline) | Our call; needs clinical sign-off beyond PHQ-9 and GAD-7 | Proposed |
| [Current score for improvement](#current-score-for-improvement) | Our call | Proposed |
| [Fifty percent improved](#fifty-percent-improved) | Our call | Proposed |
| [Paired forms](#paired-forms) | NYS says, for improvement | Proposed |
| [Remission timing](#remission-timing) | Our call | Proposed |
| [Remission needs an elevated baseline](#remission-needs-an-elevated-baseline) | Our call | Proposed |
| [Remission thresholds](#remission-thresholds) | Our call; needs clinical sign-off beyond PHQ-9 and GAD-7 | Proposed |
| [Psychiatric consultation denominator](#psychiatric-consultation-denominator) | Our call | Proposed |
| **Contacts and reviews** | | |
| [Clinical contact](#clinical-contact) | Our call | Proposed |
| [Active treatment](#active-treatment) | Our call | Proposed |
| [Psychiatric case review](#psychiatric-case-review) | Our call | Proposed |
| **Screening** | | |
| [Who should be screened](#who-should-be-screened) | Our call | Proposed |
| [What counts as screened](#what-counts-as-screened) | Our call | Proposed |
| [Initial PHQ-9](#initial-phq-9) | Our call | Proposed |
| [PHQ-A counts as PHQ-9](#phq-a-counts-as-phq-9) | Our call | Proposed |
| **Staffing** | | |
| [BHCM FTE](#bhcm-fte) | Our call | Proposed |

---

## Reporting

### Reporting month

**Call.** "This month" is the calendar month in the site's local time zone. Every event
belongs to the month it happened in, not the month it was documented, signed or billed.
Convert stored timestamps (often UTC) to local time before taking the date.

**Why.** If one metric uses service dates and another uses documentation dates, a patient
can fall in one month's denominator and the next month's numerator.

**Replaces.** D-01.

### When to run the report

**Call.** Run a month's report no earlier than 15 days after the month ends, so late
notes and coding can close. Once a month is submitted, don't restate it except to correct
an error.

**Why.** Running on the 1st undercounts contacts and scales documented late.

**If NYS rules otherwise.** NYS's submission deadline (unknown; see
[open questions](../open-questions.md)) overrides the 15 days if it is sooner.

**Replaces.** D-19, D-19a.

### Rounding

**Call.** Report percentages and weeks to one decimal place, rounding half up, and
calculate from unrounded numbers. For example, 7 of 8 is 87.5%, and 2 of 3 is 66.7%.
Report BHCM FTE as attested.

**Why.** NYS doesn't say. Rounding at the last step and to the same precision everywhere
means two sites with the same counts report the same rate.

**If NYS rules otherwise.** The REDCap form's field format wins.

**Replaces.** Nothing; first raised here.

### Empty denominators

**Call.** When a metric's denominator is zero (for example, no Medicaid patient was
discharged this month, so there's nothing to average for metric 4), report no value and
say why. Don't report 0 or 0%.

**Why.** Zero would read as a result, such as "no patient improved", when there was no
one to measure.

**If NYS rules otherwise.** Follow whatever the REDCap form allows.

**Replaces.** Nothing; first raised here.

## Enrollment and discharge

### What counts as enrolled

**Call.** A patient is enrolled from a documented CoCM enrollment (in a registry, or a
structured program-enrollment record in the EHR) until discharged. A referral is not an
enrollment, and neither is verbal consent with nothing recorded. A site with no
enrollment record may infer enrollment from CoCM billing codes (99492, 99493, 99494,
G2214), but must disclose that it did.

**Why.** Counting from referral inflates enrollment; counting only billed months
undercounts it, because an enrolled patient can go a month unbilled.

**Replaces.** D-02, D-02a.

### Enrollment date

**Call.** The enrollment date is the date of the initial assessment by the BHCM. If the
assessment takes more than one contact, it's the first contact at which a
symptom-monitoring scale was given. It is the start date for every metric, not just
metric 4.

**NYS says.** Metric 4 counts weeks "between initial assessment to date of discharge."

**Why.** One start date for all metrics. Using the referral date or the date the record
was keyed in shortens or lengthens every patient's time in treatment.

**Replaces.** D-03.

### Enrolled this month

**Call.** A patient is enrolled this month if their enrollment overlaps the month by at
least one day: enrolled on or before the last day, and not discharged before the first
day.

**Why.** Metrics 5 and 7 measure what happened during the month. A patient treated on the
5th who graduates on the 20th should count. A month-end snapshot would drop them.

**Replaces.** D-05, D-05a.

### Inactivity discharge

**Call.** A patient with no [clinical contact](#clinical-contact) for 90 consecutive days
is discharged, with a discharge date of the last clinical contact plus 90 days. A patient
with no clinical contact since enrollment is discharged 90 days after the enrollment
date.

**Why.** Patients who stop engaging but are never discharged inflate enrollment and pull
the contact rate down. Setting the date at day 90, rather than backdating it to the last
contact, means months already reported don't change.

**Replaces.** D-04, D-04a.

### Seventy days

**Call.** A patient has been "enrolled for 70 days or greater" when at least 70 days have
elapsed from the enrollment date to the last day of the month, or to the discharge date
if they were discharged in the month. For example, a patient enrolled on 1 January 2025
reaches 70 days on 12 March 2025. "At least 10 weeks" in Appendix A means the same.

**Why.** The draft counted the enrollment date as day 1, so patients reached "day 70"
after 69 days.

**Replaces.** D-06, R-07.

### Diagnosed and enrolled

**Call.** Metric 3 counts Medicaid patients whose enrollment date is in the month.
"Diagnosed" adds nothing that has to be measured, because enrollment requires a
qualifying behavioral health diagnosis.

**NYS says.** "Number of Medicaid patients who were diagnosed and enrolled in CoCM this
month."

**Why.** Few systems record a reliable diagnosis date. Where it exists, it's often the
date a code was added to the problem list, which says little about when CoCM started.

**If NYS rules otherwise.** If NYS means the diagnosis must also be new this month, the
data contract's optional `diagnosis_date` column covers it.

**Replaces.** R-09, Q-06.

### Duration in weeks

**Call.** For each Medicaid patient discharged in the month, count the days from
enrollment date to discharge date. Average those days, divide by 7, and round to one
decimal place. For example, patients with 84 and 91 days average 87.5 days, which is
12.5 weeks.

**Why.** Converting each patient to whole weeks first, or rounding at different steps,
gives different answers from the same data.

**Replaces.** R-08.

## Medicaid

### Who counts as Medicaid

**Call.** A patient is a Medicaid patient for the month if they have active New York
State Medicaid coverage on the first day of the month, whether fee-for-service or a
Medicaid managed care plan, and whether it is their primary or secondary coverage. Dual
Medicare–Medicaid patients count. Child Health Plus and the Essential Plan do not. A
patient whose coverage changes mid-month keeps their first-of-month status. Use the
coverage known at the run date; Medicaid granted retroactively later doesn't restate a
submitted month.

**Why.**
- First of the month: payer as of the report run date reclassifies patients after the fact.
- Primary or secondary: the draft said "primary coverage" and also said dual eligibles count, but for most dual eligibles Medicare is primary. Any active Medicaid coverage resolves the contradiction.
- Child Health Plus and the Essential Plan are separate programs, not Medicaid.
- Managed care plans are listed by plan name (Fidelis, Healthfirst and so on), so map them by plan, not by looking for the word "Medicaid".

**Replaces.** D-07, D-07a.

### Remission is a Medicaid metric

**Call.** Metric 7 counts Medicaid patients only, like metrics 2 to 8.

**NYS says.** The description says "patients enrolled in treatment"; the numerator and
denominator both say "Medicaid patients".

**Why.** The numerator and denominator are the operative definition, and the metric sits
with the other Medicaid metrics in the source.

**Replaces.** Nothing; first raised here.

## Scales and outcomes

### Primary scale

**Call.** Each episode has one primary scale, recorded at enrollment and never changed
during the episode. It is the scale the clinic uses to treat the primary diagnosis. When
a site has no record of which that is, use this default:

| Primary diagnosis | Primary scale |
|---|---|
| Depression, adult | PHQ-9 |
| Depression, adolescent | PHQ-9 or SMFQ; the site picks one and uses it for every adolescent |
| Anxiety, adult | GAD-7 |
| Anxiety, child or adolescent | SCARED |
| PTSD | PCL-5 |
| ADHD | NICHQ Vanderbilt |
| General pediatric behavioral concern | PSC-17 |

**NYS says.** Patients count toward improvement "when they meet criteria for the scale
used to treat their primary diagnosis."

**Why.** Assessing improvement on whichever scale improved most inflates the rate.
Changing the scale mid-episode loses the baseline.

**Replaces.** D-13, D-13a.

### Baseline

**Call.** The baseline is the first score on the primary scale dated on or within 14
days after the enrollment date. If there is none in that window, it is the first score
on the primary scale after enrollment. A score from before the enrollment date, such as
the screening PHQ-9 that led to the referral, is never the baseline. A re-enrollment is
a new episode with a new baseline.

**Why.** A screening score can be weeks old and was taken for a different purpose. Tying
the baseline to the episode stops it carrying over between enrollments.

**Replaces.** D-12, D-12a.

### Elevated baseline

**Call.** A baseline is elevated when it is at or above the scale's threshold:

| Scale | Elevated at or above | Firmness |
|---|---|---|
| PHQ-9 | 10 | Our call |
| GAD-7 | 10 | Our call |
| PCL-5 | 33 | Needs clinical sign-off |
| SCARED (either form) | 25 | Needs clinical sign-off |
| PSC-17 | 15 | Needs clinical sign-off |
| SMFQ (child form) | 12 | Needs clinical sign-off |
| SMFQ (parent form), NICHQ Vanderbilt | none yet | Needs clinical sign-off |

Each value is a published screening cutoff for the instrument; the
[instruments](instruments.md#where-the-thresholds-come-from) page gives the sources.
Until a scale has a threshold, its patients can't count as improved or in remission.

**NYS says.** Appendix A includes only patients "who had an elevated baseline score", but
doesn't say what elevated means.

**Why.**
- PHQ-9 and GAD-7: 10 mirrors Appendix A's "score below 10" improvement criterion, so a patient can't qualify as improved at baseline.
- PCL-5, SCARED and PSC-17: each threshold is the instrument's published screening cutoff, and it matches the remission threshold the draft proposed. That pairs naturally: elevated is at or above the cutoff, remission is below it.
- SMFQ: 12 is supported for adolescents seeking help, but the instrument's developers recommend no single cutpoint. It needs a clinician's judgement more than the others.
- The draft promised these thresholds in an appendix that was never written.

**Replaces.** D-12b, R-12 (in part).

### Current score for improvement

**Call.** Improvement compares the baseline with the most recent score on the primary
scale dated after the baseline and on or before the last day of the month. If there is
no score this month, the most recent earlier score in the episode is used. A patient with
no score after their baseline has not improved.

**Why.** Unlike remission, improvement isn't worded "this month" in the source, and a
patient who improved in month 3 and missed a scale in month 4 has not stopped improving.
Metric 5 already penalizes the missing scale.

**Replaces.** D-15, D-15a.

### Fifty percent improved

**Call.** "Score 50% improved from baseline" means the current score is at most half
the baseline. The boundary counts: a PHQ-9 baseline of 15 is improved at 7.5 or below,
which in whole scores is 7 or below.

**NYS says.** "Score 50% improved from baseline", without saying whether exactly 50%
counts.

**Why.** "Improved by 50%" reads naturally as "by at least 50%". Stating it stops one
site using "less than" and another "at most".

**Replaces.** Nothing; first raised here.

### Paired forms

**Call.** SCARED, SMFQ and the NICHQ Vanderbilt each have more than one form (child and
caregiver, or parent and teacher). Each form has its own baseline. A patient meets the
criteria if either form does, compared against that same form's baseline. The forms don't
have to be completed on the same date.

**NYS says.** Appendix A: SCARED "caregiver and/or youth"; SMFQ child **OR** parent;
Vanderbilt parent **OR** teacher.

**Why.** It's what Appendix A says, applied consistently to remission too.

**Replaces.** Q-08 (in part), Q-09.

### Remission timing

**Call.** A patient is in remission this month only if they have a score on the primary
scale dated in the month that meets the remission threshold. If they have more than one,
use the last.

**NYS says.** "Achieved remission criteria during this month."

**Why.** The draft carried the most recent score forward with no limit, so a score from
months ago could keep a patient in remission indefinitely. That isn't what the source
says.

**Replaces.** R-03, Q-02, and D-16 (in part).

### Remission needs an elevated baseline

**Call.** Only a patient with an [elevated baseline](#elevated-baseline) can count in the
remission numerator. The denominator stays as NYS defines it: every Medicaid patient
enrolled this month.

**Why.**
- Without the guard, a patient who enrolls with a PHQ-9 of 4 is "in remission" on day one.
- The denominator is left alone because NYS states it explicitly ("enrolled in treatment for any length of time").
- As a result, patients on scales with no signed-off threshold can't yet count as in remission. That holds the rate down rather than inflating it.

**Replaces.** R-04, Q-03.

### Remission thresholds

**Call.**

| Scale | Remission below | Firmness |
|---|---|---|
| PHQ-9 | 5 | Our call |
| GAD-7 | 5 | Our call |
| PCL-5 | 33 | Needs clinical sign-off |
| SCARED | 25 | Needs clinical sign-off |
| PSC-17 | 15 | Needs clinical sign-off |
| SMFQ (child form) | 8 | Needs clinical sign-off |
| NICHQ Vanderbilt | fewer than 6 symptom items rated 2 or 3 | Needs clinical sign-off |

[Paired forms](#paired-forms) apply: either form meeting the threshold counts.

**NYS says.** Nothing; remission criteria aren't defined anywhere in the source.

**Why.**
- PHQ-9: below 5 is the HEDIS depression remission definition (DRR-E).
- GAD-7: below 5 is the instrument's "minimal" band.
- PCL-5, SCARED and PSC-17: below each instrument's screening cutoff.
- SMFQ (below 8) and the Vanderbilt rule: the draft's proposals, with no source yet. The Vanderbilt rule also needs a symptom count, not a total score (Q-08).

Sources are on the [instruments](instruments.md#where-the-thresholds-come-from) page. Every
threshold beyond PHQ-9 and GAD-7 needs a clinician's review.

**Replaces.** D-16, D-16a, Q-08 (in part).

### Psychiatric consultation denominator

**Call.** The metric 8 denominator is the metric 6 denominator minus the metric 6
numerator: Medicaid patients enrolled for [70 days or more](#seventy-days), with an
[elevated baseline](#elevated-baseline), who did not meet improvement criteria this month.

**NYS says.** Patients "who have not met clinical improvement criteria this month", with a
pointer to Appendix A, which only assesses patients with an elevated baseline.

**Why.** Including patients with no elevated baseline would put patients in the
denominator who can never be assessed as improved.

**Replaces.** R-06, Q-05.

## Contacts and reviews

### Clinical contact

**Call.** A clinical contact is a documented, synchronous interaction in which the BHCM
(or another CoCM clinician) delivers treatment to the patient or, for a child, the
caregiver: in person, by video or by phone. There is no minimum duration; the
documentation of treatment content is the test.

These don't count:
- scheduling and reminder calls;
- no-shows and unanswered outreach;
- portal messages, texts and email, even with clinical content;
- the psychiatric consultant's case review, which is a review, not a patient contact.

**NYS says.** "A contact in which symptom monitoring may occur and treatment is delivered
with corroborating documentation in the patient chart. This includes virtual engagement
if treatment is delivered."

**Why.**
- Outreach attempts are the most common way the contact rate gets inflated.
- Excluding messages is new; the draft excluded only messages "without clinical content". It's hard to show that treatment was delivered in an asynchronous message, and a reviewer would have to read each one to decide.

**Replaces.** D-14, D-14a.

### Active treatment

**Call.** For metric 5, a patient needs both a [clinical contact](#clinical-contact) and a
scored scale in the month. They don't have to be on the same day. The scale can be any
of the seven NYS instruments, not only the primary scale, but it must be dated on or
after the enrollment date.

**NYS says.** "At least one clinical contact and symptom-monitoring scale completed this
month," with the list of appropriate scales.

**Why.**
- NYS lists the scales without tying them to the primary diagnosis.
- Requiring the same day would penalize sites that send scales before the session.
- A screening score from before enrollment isn't a monitoring score.

**Replaces.** D-11 (in part).

### Psychiatric case review

**Call.** A case review counts when the psychiatric consultant reviewed this patient and
documented a recommendation to the PCP or BHCM. "Continue current treatment" is a
recommendation. The review must fall within the 60 days ending on the last day of the
month, counting both ends. For March 2025, that is 31 January to 31 March.

**NYS says.** "Reviewed by the Psychiatric Consultant with treatment recommendations
provided to the PCP or BHCM in the past 60 days."

**Why.** The consultant attending a caseload meeting is not a review of every patient on
the caseload. Counting back from the run date instead of month end shifts the window.

**Replaces.** D-17.

## Screening

### Who should be screened

**Call.** The metric 9 denominator is each patient, counted once, who had at least one
qualifying visit in the month and was 12 or older on the visit date. No other exclusions.

A qualifying visit is an in-person or telehealth visit with a medical (not behavioral
health) provider, billed with one of these codes:
- office or outpatient evaluation and management (E&M), 99202–99215, except 99211,
  which is normally billed for a nurse-only visit;
- preventive medicine, 99381–99397;
- annual wellness visit, G0438 and G0439;
- their telehealth equivalents.

Nurse-only visits, lab and vaccine visits, and visits with the BHCM or any behavioral
health clinician aren't qualifying visits. The code list is the draft's, and will be
checked when the screening page is written.

**NYS says.** "Patients seen in the practice for any reason this month that meet practice
criteria for universal depression screen (Refer to practice workflow)."

**Why.**
- NYS leaves the criteria to each practice. Publishing one set means two practices' rates mean the same thing.
- Screening happens at medical visits, so lab, nurse and BHCM visits only inflate the denominator.
- 12 matches USPSTF adolescent screening.
- The draft defined visits but never said to count each patient once.

**If NYS rules otherwise.** If NYS means every patient seen "for any reason", the data
contract already extracts every visit with its provider type and codes.

**Replaces.** D-08, D-08a, D-09, D-09a, D-09b, R-01, R-02, Q-01.

### What counts as screened

**Call.** A patient in the metric 9 denominator is screened if they have a scored PHQ-2
or PHQ-9 dated in the 12 months ending on the last day of the month, by anyone, for any
reason. That includes a CoCM monitoring PHQ-9. A declined screen does not count. A
positive PHQ-2 with no follow-up PHQ-9 still counts as screened.

**NYS says.** "Received a PHQ-2 or 9 either during this visit **or** have been screened
in the last 12 months."

**Why.**
- The draft excluded CoCM patients' monitoring PHQs, so a patient with a PHQ-9 last week counted as unscreened. That penalizes the practices with the most active CoCM programs.
- One window ending at month end is simpler than one per visit, and it includes a screen at a later visit the same month.

**Replaces.** D-10 (for metric 9), R-05, Q-04.

### Initial PHQ-9

**Call.** A PHQ-9 is a patient's initial PHQ-9 if it is dated in the month and the
patient has no other scored PHQ-9 in the 365 days before it. Each patient counts at
most once a month. Context doesn't matter: a PHQ-9 given by a medical provider or by the
BHCM counts the same.

**NYS says.** "Patients who received their initial PHQ-9 during this month."

**Why.**
- "First ever" can't be known from most systems.
- "First this month" would count a CoCM patient's monthly monitoring PHQ-9 every month.
- 365 days lines up with the annual screening in metric 9.

**Consequence.** With this rule and [what counts as screened](#what-counts-as-screened),
neither screening metric needs to know whether a PHQ was for screening or monitoring.
That distinction now matters only for the [baseline](#baseline), and there the date
alone decides it.

**Replaces.** D-10 (for metric 10), R-10, Q-07.

### PHQ-A counts as PHQ-9

**Call.** The PHQ-9 Modified for Adolescents (PHQ-A) counts as a PHQ-9 for metrics 9
and 10, and as the PHQ-9 when it is an adolescent's primary scale.

**Why.** With a screening age floor of 12, many sites screen adolescents with the PHQ-A,
which is scored the same way. Excluding it would undercount screening at every site that
sees adolescents.

**Replaces.** Nothing; first raised here.

## Staffing

### BHCM FTE

**Call.** Metric 11 is the sum of CoCM care-management effort by staff in the BHCM role.
Each BHCM counts as the share of a full-time schedule spent on CoCM: a BHCM at 60% CoCM
contributes 0.6. Psychiatric consultants, PCPs, supervisors' supervisory time, trainees,
and care coordinators or community health workers who support the BHCM are not counted.
A supervisor who also carries a CoCM caseload counts for the share spent as a BHCM.
Use scheduled effort, prorated for start and end dates, extended leave and vacancies;
ordinary vacation days aren't deducted. The site attests the figure.

**Why.** It matches the optimal caseload NYS states (more than 75 patients per BHCM FTE),
which is about care-manager capacity.

**Replaces.** D-18, D-18a.
