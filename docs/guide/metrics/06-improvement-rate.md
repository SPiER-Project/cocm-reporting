# 6. Improvement rate

> Proportion (%) of Medicaid patients enrolled in treatment for 70 days or greater who
> demonstrated clinically significant improvement on relevant symptom-monitoring scale.
> *(2025 Target Rate: ≥ 60%)*
>
> — [NYS, metric 6](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#6-improvement-rate),
> and [Appendix A](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#appendix-a-improvement-rate-specifications)

**Reported as:** a percentage. **Target:** 60% or more. **Population:** CoCM, Medicaid,
70 days or more, with an elevated baseline.

## The rule

- **Denominator:** Medicaid patients enrolled this month who have both of these:
  - [70 days or more](../concepts/enrollment-and-discharge.md#seventy-days) in treatment,
    measured to month end or to discharge;
  - an [elevated baseline](../concepts/scales-and-outcomes.md#elevated-baseline) on their
    [primary scale](../concepts/scales-and-outcomes.md#primary-scale).
- **Numerator:** those whose current primary-scale score meets the
  [improvement criteria](../concepts/scales-and-outcomes.md#improvement-metrics-6-and-8)
  in NYS Appendix A, compared with their [baseline](../concepts/scales-and-outcomes.md#baseline).

The current score is the most recent primary-scale score on or before month end. If
there's none this month, the last earlier score in the episode carries forward. A patient
with no score since baseline hasn't improved.

Only the primary scale counts. A patient being treated for depression who improves on
the GAD-7 but not the PHQ-9 has not improved.

## Worked example

From the [example caseload](../example-caseload.md):

| Patient | Days | Baseline | Current | Improved? |
|---|---|---|---|---|
| P1 | 147 | PHQ-9 18 | 8 | **Yes**: below 10 |
| P3 | 84 | PHQ-9 15 | 7 | **Yes**: below 10, and at most half of 15 |
| P4 | 160, to discharge | GAD-7 16 | 12 (December, carried forward) | No: not below 10, and more than half of 16 |
| P6 | 119 | PCL-5 48 | 40 | No: 8 points better; needs 12 |
| P7 | 196 | PHQ-9 12 | 3 | **Yes** |
| P9 | 102, to discharge | PHQ-9 13 | 4 | **Yes** |

Not in the denominator:
- P2: 19 days.
- P8: 105 days, but a baseline of 8 isn't elevated.
- P5: not Medicaid.

**Metric 6: 4 of 6, 66.7%.**

## Where the data lives

Scores from the registry's scale table, or EHR questionnaires and flowsheets; primary
diagnosis and scale from the episode. See
[scales and outcomes](../concepts/scales-and-outcomes.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting improvement on any scale, not the primary one | Overstated |
| Comparing with last month instead of baseline | Understated for patients who improved early and held steady |
| Using a pre-enrollment screening score as baseline | Usually overstated |
| Including patients without an elevated baseline | Overstated: a patient enrolled with a PHQ-9 of 8 is "below 10" on day one |
| Counting from referral, so patients reach 70 days early | Understated: patients enter the denominator before treatment has had time to work |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment)
(`primary_scale`), [`coverage`](../../reference/data-contract.md#t2-coverage), [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient) (for
the inactivity discharge) and
[`scale_result`](../../reference/data-contract.md#t5-scale_result--one-row-per-completed-scored-administration),
from each open episode's enrollment date onward.
