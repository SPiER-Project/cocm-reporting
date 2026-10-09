# Scales and outcomes

The symptom scales, and how they become improvement and remission. This is where two
sites with the same patients are most likely to report different numbers. Each step
below (which scale, which score is the baseline, which score is current) is a choice a
report writer would otherwise make alone.

**Used by:** metrics 5 to 8. Metric 5 needs only "a scale was completed"; metrics 6 to 8
use everything on this page.

## What NYS says

- Metric 5 lists the appropriate scales: PHQ-9, GAD-7, PCL-5, SMFQ, SCARED, PSC-17 and
  NICHQ Vanderbilt.
- Appendix A gives the improvement criteria for each scale. It includes only patients
  "who had an elevated baseline score" and in treatment at least 10 weeks. Patients count
  "when they meet criteria for the scale used to treat their primary diagnosis."
- Metric 7 asks for patients who "achieved remission criteria during this month". NYS
  doesn't define remission criteria anywhere.

([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#appendix-a-improvement-rate-specifications))

## The rule

### A scale result

A scale result is **a completed administration with a total score and a date**. A form
that was offered, ordered or partly completed, with no total score, doesn't count. Nor
does a note that says "PHQ-9 administered" with no score.

| Scale | Forms | Typically used for |
|---|---|---|
| PHQ-9 | One. The adolescent version (PHQ-A) counts as a PHQ-9 | Depression |
| GAD-7 | One | Anxiety |
| PCL-5 | One | PTSD |
| SMFQ | Child (SMFQ-C) and parent (SMFQ-P) | Adolescent depression |
| SCARED | Child and caregiver | Child and adolescent anxiety |
| PSC-17 | One | General pediatric behavioral concerns |
| NICHQ Vanderbilt | Parent (Vanderbilt-P) and teacher (Vanderbilt-T) | ADHD |

### Primary scale

Each episode has **one primary scale**, recorded at enrollment and kept for the whole
episode. It is the scale the clinic uses to treat the primary diagnosis. If a site has
no record of which that is, use the default:

| Primary diagnosis | Primary scale |
|---|---|
| Depression, adult | PHQ-9 |
| Depression, adolescent | PHQ-9 or SMFQ. The site picks one and uses it for every adolescent |
| Anxiety, adult | GAD-7 |
| Anxiety, child or adolescent | SCARED |
| PTSD | PCL-5 |
| ADHD | NICHQ Vanderbilt |
| General pediatric behavioral concern | PSC-17 |

*Our call: [primary scale](../../reference/our-calls.md#primary-scale).* A patient may
complete other scales too. They count for metric 5, but improvement and remission are
judged only on the primary scale.

### Baseline

The baseline is **the first primary-scale score on or within 14 days after the enrollment
date**. If there's none in that window, it's the first primary-scale score after
enrollment. A score from before the enrollment date, such as the screening PHQ-9 that led
to the referral, is never the baseline. *Our call:
[baseline](../../reference/our-calls.md#baseline).*

For scales with two forms, each form has its own baseline.

### Elevated baseline

Only a patient with an **elevated baseline** can count as improved or in remission.

| Scale | Elevated at or above | Firmness |
|---|---|---|
| PHQ-9 | 10 | Our call |
| GAD-7 | 10 | Our call |
| PCL-5 | 33 | Needs clinical sign-off |
| SCARED | 25 | Needs clinical sign-off |
| PSC-17 | 15 | Needs clinical sign-off |
| SMFQ (child form) | 12 | Needs clinical sign-off |
| SMFQ (parent form), NICHQ Vanderbilt | not yet set | Needs clinical sign-off |

*[Elevated baseline](../../reference/our-calls.md#elevated-baseline).* The values marked
for sign-off are each instrument's published screening cutoff (sources on the
[instruments](../../reference/instruments.md#where-the-thresholds-come-from) page), but a
clinician still needs to agree to use them this way. Until a scale has a threshold,
patients on that scale can't be counted as improved or in remission.

### Improvement (metrics 6 and 8)

Compare the baseline with **the current score**: the most recent primary-scale score
after the baseline, on or before the last day of the month. If there's no score this
month, the most recent earlier score in the episode is current. A patient with no score
since baseline has not improved. *Our call:
[current score for improvement](../../reference/our-calls.md#current-score-for-improvement).*

| Scale | Improved when (NYS Appendix A) |
|---|---|
| PHQ-9 | Current score is at most half the baseline, **or** below 10 |
| GAD-7 | Current score is at most half the baseline, **or** below 10 |
| PCL-5 | Current score is at least 12 points below baseline |
| NICHQ Vanderbilt | Parent **or** teacher form is at most half its baseline |
| SCARED | Caregiver **and/or** child form is at most half its baseline |
| SMFQ | Child form at least 8 points below its baseline, **or** parent form at least 6 points below its baseline |
| PSC-17 | Current score is at most half the baseline |

"50% improved" means the current score is at most half the baseline, so a PHQ-9
baseline of 15 is improved at 7 or below. *NYS says*, except for that reading, which is
*our call: [fifty percent improved](../../reference/our-calls.md#fifty-percent-improved).*

### Paired forms

For SCARED, SMFQ and the Vanderbilt, **either form meeting its criteria counts**, compared
against that same form's baseline. The forms don't have to be completed on the same day.
*NYS says, for improvement; our call to apply it to remission:
[paired forms](../../reference/our-calls.md#paired-forms).*

### Remission (metric 7)

A patient is in remission this month when all three hold:

1. They have an [elevated baseline](#elevated-baseline).
2. They have a **primary-scale score dated this month**. If there's more than one, use
   the last.
3. That score is **below the remission threshold**:

| Scale | Remission below | Firmness |
|---|---|---|
| PHQ-9 | 5 | Our call |
| GAD-7 | 5 | Our call |
| PCL-5 | 33 | Needs clinical sign-off |
| SCARED | 25 | Needs clinical sign-off |
| PSC-17 | 15 | Needs clinical sign-off |
| SMFQ (child form) | 8 | Needs clinical sign-off |
| NICHQ Vanderbilt | fewer than 6 symptom items rated 2 or 3 | Needs clinical sign-off |

*Our calls: [remission timing](../../reference/our-calls.md#remission-timing),
[remission needs an elevated baseline](../../reference/our-calls.md#remission-needs-an-elevated-baseline),
[remission thresholds](../../reference/our-calls.md#remission-thresholds).*

Unlike improvement, remission **doesn't carry forward**: no score this month, no
remission. The metric 7 denominator is every Medicaid patient enrolled this month, as NYS
states. The elevated-baseline requirement applies only to the numerator.

### Not improved (metric 8)

The metric 8 population is metric 6's denominator minus its numerator: Medicaid patients
enrolled 70 days or more, with an elevated baseline, who have not improved this month.
*Our call: [psychiatric consultation denominator](../../reference/our-calls.md#psychiatric-consultation-denominator).*

## Worked example

One adult patient whose primary scale is PHQ-9. Enrolled 6 January 2025.

| Date | PHQ-9 | What it is |
|---|---|---|
| 20 Dec 2024 | 16 | Screening at a PCP visit. Before enrollment, so not the baseline |
| 13 Jan 2025 | 15 | **Baseline**: first PHQ-9 within 14 days of enrollment. Elevated (15 ≥ 10) |
| 10 Feb 2025 | 11 | |
| 17 Mar 2025 | 7 | |
| April | none | |

| Month | Days enrolled at month end | In metric 6? | Current score | Improved? | In remission? |
|---|---|---|---|---|---|
| February | 53 | No, under 70 days | 11 | — | No (11 isn't below 5) |
| March | 84 | Yes | 7 | **Yes**: below 10, and at most half of 15 | No (7 isn't below 5) |
| April | 114 | Yes | 7, carried forward | **Yes** | No: no score in April |

In April the patient also misses [active treatment](contacts-and-reviews.md#active-treatment-metric-5)
for metric 5, because no scale was completed.

## What the program should do

- **Record the primary scale at enrollment**, and don't change it during the episode. If
  the clinical focus really changes, close the episode and open a new one.
- **Give the primary scale within two weeks of enrollment**, so the baseline is the score
  the program meant it to be.
- **Give the primary scale at least monthly.** Improvement carries forward, but remission
  and metric 5 don't.
- **Record every scale as a scored, structured result**, not only in the note.
- **For paired forms, record which form each score is.** A caregiver SCARED and a child
  SCARED are different results.

## Where the data lives

| Fact | Registry | EHR without a registry |
|---|---|---|
| Scale results | The registry's assessment or scale table | Questionnaire results, flowsheet rows or observations with a structured total score |
| Which form | Usually the instrument name | Often a separate questionnaire or flowsheet row per form |
| Primary diagnosis | The episode's primary or target condition | The diagnosis linked to the CoCM episode, or the BHCM's assessment diagnosis |
| Primary scale | A primary-scale field, if the registry has one | Rarely recorded; use the default mapping from the primary diagnosis, and disclose it |

- Many registries store only PHQ-9 and GAD-7. Episodes for PTSD, ADHD or pediatric
  concerns then have no primary-scale scores at all. The
  [prototype registry mapping](../../collecting/registries/prototype-cocm-registry.md#t5-scale_result--assessmentscore)
  is an example.
- In an EHR, the same PHQ-9 questionnaire may be used by the PCP for screening and by the
  BHCM for monitoring. For this page, only the date matters: a score before the
  enrollment date is never the baseline. The screening metrics don't need the
  distinction either ([screening](screening.md)).

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting a patient improved if any scale improved | Improvement overstated |
| Comparing with last month's score instead of the baseline | Improvement understated for patients who improved early and then held steady |
| Using a pre-enrollment screening score as baseline | The baseline is older and often higher; improvement overstated |
| Including patients without an elevated baseline in improvement | Patients enrolled with mild scores count as "improved" on day one |
| Carrying a months-old score forward for remission | Remission overstated |
| Counting an unscored or partial form | Metric 5 overstated |
| Changing the primary scale mid-episode | The baseline is lost, or compared across different scales |

## For automation

- [`scale_result`](../../reference/data-contract.md#t5-scale_result--one-row-per-completed-scored-administration)
  holds every scored result. Each form is its own `instrument` value, so pairing is the
  calculator's job.
- [`cocm_episode.primary_scale`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment)
  is required. Where the source has none, the extract fills it from the default mapping,
  and the disclosure says so.
- Baseline, elevated baseline, current score, improvement and remission are all derived
  by the calculator. None of them is extracted.
- Thresholds live in calculator settings, so a clinical sign-off changes a setting, not
  an extract.
