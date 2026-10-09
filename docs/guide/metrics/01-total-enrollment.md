# 1. Total enrollment

> Total number of patients enrolled in CoCM this month, all payers.
> *(Optimal Caseload: >75 patients / 1 BHCM FTE)*
>
> — [NYS, metric 1](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#1-total-enrollment)

**Reported as:** a count. **Population:** CoCM, all payers.

## The rule

Count every patient [enrolled this month](../concepts/enrollment-and-discharge.md#enrolled-this-month),
whatever their coverage: their enrollment overlaps the month by at least one day. Count
each patient once, even if they had two episodes in the month.

The optimal caseload is a reference, not part of the metric. Divide the count by
[metric 11](11-bhcm-staffing.md) to compare.

## Worked example

From the [example caseload](../example-caseload.md):

| Patient | Counted? | Why |
|---|---|---|
| P1, P2, P3, P6, P7, P8 | Yes | Enrolled throughout or from mid-month |
| P4 | Yes | Discharged 10 March, so enrolled for part of the month |
| P5 | Yes | Commercial coverage; metric 1 is all-payer |
| P9 | Yes | Graduated 21 March |
| P10 | No | Discharged in February |

**Metric 1: <!--expect:example-caseload.m1-->9<!--/expect-->.**

## Where the data lives

The registry's enrollment or episode records, or the EHR's program-enrollment records.
See [enrollment and discharge](../concepts/enrollment-and-discharge.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Applying the Medicaid filter | Understated; that's metric 2 |
| Counting referrals, waitlisted or "planned" patients | Overstated |
| Leaving disengaged patients enrolled indefinitely | Overstated, and the contact rate falls |
| Counting only patients enrolled on the last day | Understated; patients discharged mid-month drop out |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment),
and [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient) for the inactivity discharge. Distinct `patient_id` among episodes overlapping
the month.
