# 2. Medicaid enrollment

> Total number of Medicaid patients enrolled in CoCM this month.
>
> — [NYS, metric 2](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#2-medicaid-enrollment)

**Reported as:** a count. **Population:** CoCM, Medicaid.

## The rule

[Metric 1](01-total-enrollment.md), limited to [Medicaid patients](../concepts/medicaid.md):
patients with active New York State Medicaid coverage on the first day of the month,
fee-for-service or managed care, primary or secondary.

This count is also the denominator for metrics 5 and 7.

## Worked example

From the [example caseload](../example-caseload.md): metric 1's nine patients, less P5,
who has commercial coverage. P3 is dual Medicare–Medicaid and counts; P6 is in a HARP,
which is Medicaid managed care, and counts.

**Metric 2: <!--expect:example-caseload.m2-->8<!--/expect-->.**

## Where the data lives

Enrollment from the registry or EHR; coverage from the practice-management or billing
system. The [Medicaid](../concepts/medicaid.md#what-the-program-should-do) page covers
the payer mapping this depends on.

## Common mistakes

| Mistake | Effect |
|---|---|
| Missing Medicaid managed care plans listed by plan name | Understated |
| Counting Child Health Plus or Essential Plan members | Overstated |
| Dropping dual eligibles because Medicare is primary | Understated |
| Using today's payer instead of the first of the month | Patients reclassified after the fact |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment)
and [`coverage`](../../reference/data-contract.md#t2-coverage), and [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient) for the inactivity
discharge.
