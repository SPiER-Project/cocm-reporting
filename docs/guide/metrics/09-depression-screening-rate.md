# 9. Depression screening rate

> Proportion (%) of all patients seen during the reporting period who received their
> annual PHQ-2 or PHQ-9 screening (all payers) […] *(2025 Target Rate: 85%)*
>
> — [NYS, metric 9](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#9-depression-screening-rate)

**Reported as:** a percentage. **Target:** 85%. **Population:** the whole practice, all
payers. It is not limited to CoCM patients, and the data isn't in the CoCM registry.

## The rule

- **Denominator:** [who should be screened](../concepts/screening.md#who-should-be-screened-metric-9-denominator).
  Each patient counts once if this month they had at least one qualifying visit (an E&M,
  preventive or annual wellness visit with a medical provider, but not <!--rule:who-should-be-screened.excluded_codes-->99211<!--/rule-->) and were <!--rule:who-should-be-screened.age_floor-->12<!--/rule-->
  or older on the visit date.
- **Numerator:** those [screened](../concepts/screening.md#what-counts-as-screened-metric-9-numerator):
  a scored PHQ-2 or PHQ-9 (or PHQ-A) dated in the <!--rule:what-counts-as-screened.lookback_months-->12<!--/rule--> months ending on the last day of the
  month, given by anyone, for any reason. A declined screen doesn't count.

A practice whose own screening workflow differs from this (for example, adults only)
should follow its workflow for care and disclose the difference when it reports.

## Worked example

The [screening](../concepts/screening.md#worked-example) page has the full example.

- **Denominator:** six of its eight patients. One is under 12, and one had only a nurse
  visit.
- **Numerator:** five of the six were screened, one of them through monthly CoCM PHQ-9s.
  The sixth declined.

**Metric 9: 5 of 6, 83.3%.**

## Where the data lives

All from the EHR or practice-management system:
- encounters joined to charges, with the rendering provider's type;
- patient dates of birth;
- every questionnaire, flowsheet row or observation that holds a PHQ-2, PHQ-9 or PHQ-A
  total.

See [screening](../concepts/screening.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting every encounter, including nurse, lab and BHCM visits | Understated: the denominator grows with patients nobody planned to screen |
| Counting visits instead of patients | Distorted toward frequent visitors |
| Excluding CoCM patients' monitoring PHQs | Understated: the archived draft's rule, now reversed |
| Missing a PHQ questionnaire version or a department's flowsheet | Understated |
| Counting a declined screen | Overstated |

## For automation

Reads [`patient`](../../reference/data-contract.md#t1-patient) (`birth_date`),
[`practice_visit`](../../reference/data-contract.md#t7-practice_visit--the-denominator-for-metric-9),
[`scale_result`](../../reference/data-contract.md#t5-scale_result--one-row-per-completed-scored-administration)
(<!--rule:what-counts-as-screened.lookback_months-->12<!--/rule--> months of PHQ-2, PHQ-9 and PHQ-A) and
[`site_month`](../../reference/data-contract.md#t8-site_month--one-row-per-submission)
(`screening_age_floor`).
