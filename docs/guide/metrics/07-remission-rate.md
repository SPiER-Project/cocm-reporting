# 7. Remission rate

> Proportion (%) of patients enrolled in treatment for any length of time who have
> achieved remission criteria during this month.
> **Numerator**: Number of Medicaid patients who have demonstrated remission.
> **Denominator**: Number of Medicaid patients enrolled during this month.
>
> — [NYS, metric 7](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#7-remission-rate)

**Reported as:** a percentage. **Target:** none given. **Population:** CoCM, Medicaid.

NYS doesn't define remission criteria. Every threshold below is a call, and most need
clinical sign-off. Expect this metric's rules to change more than any other's.

## The rule

- **Denominator:** [metric 2](02-medicaid-enrollment.md), every Medicaid patient enrolled
  this month, for any length of time. *Our call:
  [remission is a Medicaid metric](../../reference/our-calls.md#remission-is-a-medicaid-metric).*
- **Numerator:** those [in remission](../concepts/scales-and-outcomes.md#remission-metric-7)
  this month. All three must hold:
  1. An [elevated baseline](../concepts/scales-and-outcomes.md#elevated-baseline) on the
     primary scale.
  2. A primary-scale score **dated this month**. If there's more than one, use the last.
  3. That score is below the scale's remission threshold. For PHQ-9 and GAD-7 that's
     below <!--rule:remission-thresholds.thresholds.phq9.below-->5<!--/rule-->.

Unlike improvement, nothing carries forward. A patient in remission last month with no
score this month isn't in remission this month.

## Worked example

From the [example caseload](../example-caseload.md):

| Patient | March score | Elevated baseline? | In remission? |
|---|---|---|---|
| P1 | PHQ-9 8 | Yes | No: not below 5 |
| P2 | PHQ-9 14 | Yes | No |
| P3 | PHQ-9 7 | Yes | No |
| P4 | None | Yes | No: no score in March |
| P6 | PCL-5 40 | Yes | No: not below 33 |
| P7 | PHQ-9 3 | Yes | **Yes** |
| P8 | PHQ-9 4 | **No**, baseline 8 | No: below 5, but never had an elevated baseline |
| P9 | PHQ-9 4 | Yes | **Yes** |

**Metric 7: 2 of 8, 25.0%.**

P8 is why the elevated-baseline guard exists: without it, a patient who enrolled with
mild symptoms would count as in remission from the start.

## Where the data lives

The same scores as [metric 6](06-improvement-rate.md). See
[scales and outcomes](../concepts/scales-and-outcomes.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Carrying an old score forward | Overstated |
| Counting patients without an elevated baseline | Overstated |
| Using any scale instead of the primary scale | Overstated |
| Reporting it for all payers | The wrong population; NYS's numerator and denominator are Medicaid |
| Using a threshold of 10 (the improvement cutoff) instead of 5 | Overstated |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment),
[`coverage`](../../reference/data-contract.md#t2-coverage), [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient) (for the inactivity
discharge) and [`scale_result`](../../reference/data-contract.md#t5-scale_result--one-row-per-completed-scored-administration).
Remission thresholds are calculator settings.
