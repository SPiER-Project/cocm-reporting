# 11. BHCM staffing

> Behavioral Health Care Manager Staffing – The total BHCM FTE devoted to CoCM this month
>
> — [NYS, metric 11](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#11-behavioral-health-care-manager-staffing)

**Reported as:** FTE, as a decimal (for example, 2.1). **Population:** staff, not patients. The site
attests it.

## The rule

Add up, across staff in the BHCM role, each person's share of a full-time schedule spent
on CoCM this month. Use scheduled effort, prorated for start dates, end dates, extended
leave and vacancies. Don't count the psychiatric consultant, PCPs, supervisors'
supervision time, trainees, or support staff such as care coordinators. *Our call:
[BHCM FTE](../../reference/our-calls.md#bhcm-fte).* Details are on the
[BHCM FTE](../concepts/bhcm-fte.md) page.

**Using it with metric 1.** NYS's optimal caseload is more than 75 patients per BHCM FTE.
Divide [metric 1](01-total-enrollment.md) by this figure to compare. A ratio well below
75 can mean spare capacity; well above it, an overloaded team or patients who should
have been discharged.

## Worked example

The [BHCM FTE](../concepts/bhcm-fte.md#worked-example) page adds up three BHCMs to
**2.1 FTE**. With a total enrollment of 180, that's about 86 patients per FTE.

## Where the data lives

Staffing or HR records, or the program lead's own record. Registry time logs can be a
cross-check, but they aren't scheduled effort.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting the psychiatric consultant or support staff | Overstated |
| Counting a BHCM's whole schedule when part is non-CoCM work | Overstated |
| Leaving a vacant position in the count | Overstated |

## For automation

[`site_month.bhcm_fte`](../../data-contract.md#t8-site_month--one-row-per-submission),
typed in by the program lead.
