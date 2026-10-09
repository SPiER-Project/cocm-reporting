# 8. Psychiatric consultation rate

> Among those enrolled in treatment for 70 days or greater who did not meet clinically
> significant improvement this month (see Appendix A), proportion (%) whose case was
> reviewed by the Psychiatric Consultant with treatment recommendations provided to the
> PCP or BHCM in the past 60 days. *(2025 Target Rate: ≥ 80%)*
>
> — [NYS, metric 8](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#8-psychiatric-consultation-rate)

**Reported as:** a percentage. **Target:** 80% or more. **Population:** CoCM, Medicaid,
<!--rule:seventy-days.days-->70<!--/rule--> days or more, elevated baseline, not improved.

## The rule

- **Denominator:** [metric 6](06-improvement-rate.md)'s denominator minus its numerator:
  Medicaid patients with <!--rule:seventy-days.days-->70<!--/rule--> days or more in treatment and an elevated baseline who **have
  not improved** this month. *Our call:
  [psychiatric consultation denominator](../../reference/our-calls.md#psychiatric-consultation-denominator).*
- **Numerator:** those with a [psychiatric case review](../concepts/contacts-and-reviews.md#psychiatric-case-review-metric-8)
  in the <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days ending on the last day of the month. The review must be of this patient,
  with a recommendation to the PCP or BHCM documented. "Continue current treatment" is a
  recommendation.

For March 2025, the window is 31 January to 31 March.

## Worked example

From the [example caseload](../example-caseload.md), metric 6's two patients who didn't
improve:

| Patient | Last review | In the window? |
|---|---|---|
| P4 | 20 Nov 2024 | No |
| P6 | 5 Mar 2025, with recommendation | **Yes** |

**Metric 8: 1 of 2, 50.0%.**

P1, P3, P7 and P9 also had reviews, but they improved, so they aren't in the
denominator. P4 had no contact for three months and no review since November. The metric
is designed to surface patients like P4.

## Where the data lives

A consultation or case-review log in the registry, one row per patient discussed; in an
EHR, consultant notes, rarely a structured field. See
[contacts and reviews](../concepts/contacts-and-reviews.md#where-the-data-lives). This is
often the hardest fact to extract from an EHR alone.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting the consultant's attendance at a caseload meeting as a review of every patient | Overstated |
| Counting a review with no documented recommendation | Overstated |
| Measuring <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days back from the run date | Reviews early in the window drop out; understated |
| Including patients without an elevated baseline in the denominator | The denominator includes patients who can never improve under Appendix A |

## For automation

Reads everything [metric 6](06-improvement-rate.md) reads, plus
[`psych_review`](../../reference/data-contract.md#t6-psych_review--one-row-per-patient-discussed)
(`review_date`, `recommendation_documented = true`).
