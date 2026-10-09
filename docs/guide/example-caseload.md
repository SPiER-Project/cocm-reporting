# Example caseload

One small, invented CoCM caseload, used by every metric page from
[metric 1](metrics/01-total-enrollment.md) to [metric 8](metrics/08-psychiatric-consultation-rate.md).
Each metric page takes the slice it needs, so the eight results below all come from the
same patients.

**Reporting month:** March 2025. The metric 8 review window is 31 January to 31 March.

## The patients

| Patient | Coverage on 1 March | Enrolled | Discharged | Primary scale |
|---|---|---|---|---|
| P1 | Medicaid managed care | 4 Nov 2024 | — | PHQ-9 |
| P2 | Medicaid fee-for-service | 12 Mar 2025 | — | PHQ-9 |
| P3 | Medicare and Medicaid (dual) | 6 Jan 2025 | — | PHQ-9 |
| P4 | Medicaid managed care | 1 Oct 2024 | 10 Mar 2025, inactivity (last contact 10 Dec 2024) | GAD-7 |
| P5 | Commercial | 3 Feb 2025 | — | PHQ-9 |
| P6 | Medicaid managed care (HARP) | 2 Dec 2024 | — | PCL-5 |
| P7 | Medicaid fee-for-service | 16 Sep 2024 | — | PHQ-9 |
| P8 | Medicaid managed care | 16 Dec 2024 | — | PHQ-9 |
| P9 | Medicaid managed care | 9 Dec 2024 | 21 Mar 2025, graduated | PHQ-9 |
| P10 | Medicaid managed care | 2 Sep 2024 | 27 Feb 2025, graduated | PHQ-9 |

## Their scores and contacts

| Patient | Baseline | Elevated? | March activity | Last psychiatric review |
|---|---|---|---|---|
| P1 | 18 (12 Nov) | Yes | Phone session and PHQ-9 of 8, 10 Mar | 12 Feb, with recommendation |
| P2 | 14 (12 Mar) | Yes | Initial assessment and PHQ-9, 12 Mar; video session, 26 Mar | — |
| P3 | 15 (13 Jan) | Yes | Video session and PHQ-9 of 7, 17 Mar | 3 Mar, with recommendation |
| P4 | 16 (8 Oct) | Yes | None. Last GAD-7 was 12, on 10 Dec | 20 Nov, with recommendation |
| P5 | 13 (10 Feb) | Yes | Phone session and PHQ-9 of 11, 7 Mar | — |
| P6 | 48 (9 Dec) | Yes, with the candidate PCL-5 threshold of 33 | In-person session and PCL-5 of 40, 20 Mar | 5 Mar, with recommendation |
| P7 | 12 (16 Sep) | Yes | Phone session and PHQ-9 of 3, 24 Mar (February's was 4) | 15 Jan, with recommendation |
| P8 | 8 (18 Dec) | **No** | Video session and PHQ-9 of 4, 6 Mar | — |
| P9 | 13 (9 Dec) | Yes | Phone session and PHQ-9 of 4, 14 Mar | 26 Feb, with recommendation |
| P10 | — | — | None (discharged in February) | — |

## Derived facts

The calculator, or the report writer, derives these from the two tables above. The
concept pages explain each rule.

| Patient | Enrolled this month? | Medicaid? | Days in treatment | 70+ days? | Active treatment? | Improved? | In remission? |
|---|---|---|---|---|---|---|---|
| P1 | Yes | Yes | 147 | Yes | Yes | Yes: 8 is below 10 | No: 8 isn't below 5 |
| P2 | Yes | Yes | 19 | No | Yes | — | No |
| P3 | Yes | Yes | 84 | Yes | Yes | Yes: 7 is below 10 | No |
| P4 | Yes, discharged 10 Mar | Yes | 160, to discharge | Yes | No: no contact or scale | No: 12 is neither below 10 nor half of 16 | No: no score in March |
| P5 | Yes | No | 56 | No | Yes | — | — |
| P6 | Yes | Yes | 119 | Yes | Yes | No: 8 points better, needs 12 | No: 40 isn't below 33 |
| P7 | Yes | Yes | 196 | Yes | Yes | Yes | **Yes**: 3 is below 5 |
| P8 | Yes | Yes | 105 | Yes | Yes | Not assessed: no elevated baseline | No: 4 is below 5, but no elevated baseline |
| P9 | Yes, discharged 21 Mar | Yes | 102, to discharge | Yes | Yes | Yes | **Yes**: 4 on 14 Mar |
| P10 | No | Yes | — | — | — | — | — |

## The results

| Metric | Result | Page |
|---|---|---|
| 1. Total enrollment | 9 | [metric 1](metrics/01-total-enrollment.md) |
| 2. Medicaid enrollment | 8 | [metric 2](metrics/02-medicaid-enrollment.md) |
| 3. Newly enrolled | 1 | [metric 3](metrics/03-newly-enrolled.md) |
| 4. Average duration of treatment | 18.7 weeks | [metric 4](metrics/04-average-duration-of-treatment.md) |
| 5. Monthly contact rate | 7 of 8, 87.5% | [metric 5](metrics/05-monthly-contact-rate.md) |
| 6. Improvement rate | 4 of 6, 66.7% | [metric 6](metrics/06-improvement-rate.md) |
| 7. Remission rate | 2 of 8, 25.0% | [metric 7](metrics/07-remission-rate.md) |
| 8. Psychiatric consultation rate | 1 of 2, 50.0% | [metric 8](metrics/08-psychiatric-consultation-rate.md) |

Metrics 9 and 10 use the whole practice, not the caseload; their example is on the
[screening](concepts/screening.md#worked-example) page. Metric 11's is on the
[BHCM FTE](concepts/bhcm-fte.md#worked-example) page.
