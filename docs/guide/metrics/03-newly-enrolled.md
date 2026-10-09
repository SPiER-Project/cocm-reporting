# 3. Newly enrolled

> Number of Medicaid patients who were diagnosed and enrolled in CoCM this month.
>
> — [NYS, metric 3](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#3-newly-enrolled)

**Reported as:** a count. **Population:** CoCM, Medicaid.

## The rule

Count each [Medicaid patient](../concepts/medicaid.md) whose
[enrollment date](../concepts/enrollment-and-discharge.md#enrollment-date) (the BHCM's
initial assessment) falls in the month. "Diagnosed" adds no separate test, because
enrollment requires a qualifying diagnosis. *Our call:
[diagnosed and enrolled](../../reference/our-calls.md#diagnosed-and-enrolled).*

A returning patient who starts a new episode this month counts as newly enrolled.

## Worked example

From the [example caseload](../example-caseload.md): only P2 has an enrollment date in
March (12 March), and P2 has Medicaid. P5 enrolled in February.

**Metric 3: 1.**

## Where the data lives

The episode start date in the registry, or the date of the first BHCM encounter in the
episode. See [enrollment and discharge](../concepts/enrollment-and-discharge.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting referrals received this month | Overstated, and the patients counted aren't the ones enrolled |
| Using the date the registry record was created | Patients land in the wrong month |
| Using the date a diagnosis was added to the problem list | Patients with long-standing diagnoses are dropped |

## For automation

Reads [`cocm_episode`](../../reference/data-contract.md#t3-cocm_episode--one-row-per-enrollment)
(`enrollment_date`) and [`coverage`](../../reference/data-contract.md#t2-coverage).
