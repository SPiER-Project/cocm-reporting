# 10. Depression screening yield

> Number (#) and proportion (%) of all patients who scored a 10 or greater on their
> initial PHQ-9 during this month
>
> — [NYS, metric 10](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#10-depression-screening-yield)

**Reported as:** a count **and** a percentage. **Target:** none; this measures how much
depression screening finds, not performance. **Population:** the whole practice, all
payers.

## The rule

- **Denominator:** patients with an [initial PHQ-9](../concepts/screening.md#initial-phq-9-metric-10)
  this month. That is a scored PHQ-9 (or PHQ-A) dated this month, with no other scored
  PHQ-9 in the 365 days before it. Each patient counts once, on their first PHQ-9 of the
  month.
- **Numerator:** those whose initial PHQ-9 scored **10 or more**. *NYS says.*
- **Report both:** the numerator as the count, and numerator ÷ denominator as the
  percentage.

A PHQ-2 is never an initial PHQ-9. A CoCM patient's monthly monitoring PHQ-9 isn't
either, because there's always an earlier one within a year. That keeps the metric
about patients newly screened with the full instrument.

## Worked example

From the [screening](../concepts/screening.md#worked-example) example:

- **Patient B:** initial PHQ-9 of 14, which is positive.
- **Patient H:** initial PHQ-A of 7, which is negative.
- **Patient D:** has monthly CoCM PHQ-9s, so their March PHQ-9 isn't initial.
- **Patient A:** had only a PHQ-2.

**Metric 10: 1 patient, 1 of 2, 50.0%.**

## Where the data lives

The same PHQ results as [metric 9](09-depression-screening-rate.md), with at least 13
months of PHQ-9 history, so that the 365 days before any PHQ-9 in the month are covered.
See [screening](../concepts/screening.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Treating every PHQ-9 in the month as initial | Dominated by repeat and monitoring scores; yield distorted |
| Counting PHQ-2 results | Wrong instrument; PHQ-2 has a different scale |
| Pulling too little history to see the prior 365 days | PHQ-9s are wrongly counted as initial |
| Reporting only the percentage | NYS asks for the count too |

## For automation

Reads [`scale_result`](../../data-contract.md#t5-scale_result--one-row-per-completed-scored-administration)
(PHQ-9 and PHQ-A, with history back 365 days from the earliest PHQ-9 in the month).
