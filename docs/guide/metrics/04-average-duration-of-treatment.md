# 4. Average duration of treatment

> For Medicaid patients discharged from CoCM this month, average number of weeks between
> initial assessment to date of discharge.
>
> — [NYS, metric 4](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#4-average-duration-of-treatment)

**Reported as:** weeks, to one decimal place. **Population:** CoCM, Medicaid, discharged
this month.

## The rule

1. Take each [Medicaid patient](../concepts/medicaid.md) with a
   [discharge date](../concepts/enrollment-and-discharge.md#discharge) in the month, for
   any reason, including inactivity.
2. For each, count the days from the
   [enrollment date](../concepts/enrollment-and-discharge.md#enrollment-date) to the
   discharge date.
3. Average the days, divide by 7, and round to one decimal place.

*Our call: [duration in weeks](../../reference/our-calls.md#duration-in-weeks).* If no
Medicaid patient was discharged this month, there is nothing to average: report no value,
not zero. *Our call: [empty denominators](../../reference/our-calls.md#empty-denominators).*

## Worked example

From the [example caseload](../example-caseload.md):

| Patient | Enrolled | Discharged | Days |
|---|---|---|---|
| P4 | 1 Oct 2024 | 10 Mar 2025, inactivity | 160 |
| P9 | 9 Dec 2024 | 21 Mar 2025, graduated | 102 |

(160 + 102) ÷ 2 = 131 days; 131 ÷ 7 = 18.71.

**Metric 4: 18.7 weeks.**

P4's 90 days without contact are part of the 160. Inactivity discharges always lengthen
the average. That's accurate, because the patient was on the caseload, but a program
that discharges disengaged patients sooner will see a shorter duration.

## Where the data lives

The episode start and end dates. See
[enrollment and discharge](../concepts/enrollment-and-discharge.md#where-the-data-lives).
Watch for episodes closed without an end date; don't fill the gap with the date the
record was last updated.

## Common mistakes

| Mistake | Effect |
|---|---|
| Measuring from the referral date | Overstated |
| Leaving out inactivity discharges | Understated, and the patients most likely to need attention disappear from the metric |
| Converting each patient to whole weeks before averaging | Slightly understated |
| Backdating discharges to the last contact | Understated, and earlier months change |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment)
(`enrollment_date`, `discharge_date`), [`coverage`](../../reference/data-contract.md#t2-coverage),
and [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient): the effective discharge date is the earlier of the recorded date and the
inactivity date.
