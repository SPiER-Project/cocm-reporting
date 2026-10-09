# BHCM FTE

How much behavioral health care manager (BHCM) time the practice devotes to CoCM. It's
reported on its own as metric 11, and it's the yardstick NYS uses for caseload size.

**Used by:** metric 11, and the optimal-caseload reference in metric 1.

## What NYS says

- Metric 11: "The total BHCM FTE devoted to CoCM this month."
- Metric 1: "Optimal Caseload: >75 patients / 1 BHCM FTE."

([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#11-behavioral-health-care-manager-staffing))

## The rule

BHCM FTE is the **sum, across staff in the BHCM role, of the share of a full-time schedule
each spends on CoCM** this month. 1.0 is the site's standard full-time schedule. *Our
call: [BHCM FTE](../../reference/our-calls.md#bhcm-fte).*

| Counts | Doesn't count |
|---|---|
| A full-time BHCM working only on CoCM: 1.0 | The psychiatric consultant |
| A full-time BHCM spending 60% of the week on CoCM: 0.6 | PCPs |
| A half-time BHCM working only on CoCM: 0.5 | Supervisors' supervision time |
| A supervisor who also carries a CoCM caseload: the share spent as a BHCM | Trainees |
| | Care coordinators and community health workers who support the BHCM |

Use the effort **scheduled for the month**, adjusted for extended leave or a vacancy. A
BHCM on leave for half the month contributes half their usual share. Ordinary vacation
days are not adjusted.

The site attests the figure; no system calculates it.

## Worked example

| Staff | Role | Schedule | Share on CoCM | Contributes |
|---|---|---|---|---|
| Jordan | BHCM | Full-time | 100% | 1.0 |
| Sam | BHCM | Full-time | 60% CoCM, 40% integrated behavioral health | 0.6 |
| Riley | BHCM, started mid-March | Full-time | 100% | 0.5 (about half the month) |
| Dr. Lee | Psychiatric consultant | — | — | 0 |
| Alex | Care coordinator | Full-time | Supports the BHCMs | 0 |

Metric 11: **2.1**. With a total enrollment of 180, that's about 86 patients per BHCM FTE,
which is above NYS's optimal caseload of more than 75.

## What the program should do

- Keep a simple monthly record of each BHCM's CoCM share, and of start dates, end dates
  and extended leave.
- Recheck the shares when someone's role changes. A BHCM who picks up other duties is
  the usual reason the figure drifts.

## Where the data lives

Staffing or HR records, or the program lead's own record. Logged time (for example,
minutes per patient in a registry) can be a cross-check, but it isn't scheduled effort,
and it's usually lower because not every minute is logged.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting the psychiatric consultant, PCPs or support staff | FTE overstated; caseload per FTE looks too low |
| Counting a BHCM's whole schedule when part of it is non-CoCM work | FTE overstated |
| Leaving a vacant position in the count | FTE overstated in the months it's empty |

## For automation

- [`site_month.bhcm_fte`](../../reference/data-contract.md#t8-site_month--one-row-per-submission) is
  attested and typed in. The calculator reports caseload per FTE alongside metric 1.
