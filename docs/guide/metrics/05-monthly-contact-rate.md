# 5. Monthly contact rate

> Proportion (%) of Medicaid patients receiving active treatment in CoCM. Active
> treatment defined as patients who have had at least one clinical contact and
> symptom-monitoring scale completed this month. […] *(2025 Target Rate: ≥ 80%)*
>
> — [NYS, metric 5](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#5-monthly-contact-rate),
> which also defines a clinical contact and lists the scales

**Reported as:** a percentage. **Target:** 80% or more. **Population:** CoCM, Medicaid.

## The rule

- **Denominator:** [metric 2](02-medicaid-enrollment.md), every Medicaid patient enrolled
  this month.
- **Numerator:** those in [active treatment](../concepts/contacts-and-reviews.md#active-treatment-metric-5)
  this month. That means both of these, not necessarily on the same day:
  - a [clinical contact](../concepts/contacts-and-reviews.md#clinical-contact), which is a
    live session in which treatment was delivered and documented; outreach attempts,
    scheduling calls and messages don't count;
  - a [scored scale](../concepts/scales-and-outcomes.md#a-scale-result), on any of the seven
    NYS scales, dated on or after the enrollment date.

A patient enrolled or discharged partway through the month is in the denominator, and
needs both within the days they were enrolled.

## Worked example

From the [example caseload](../example-caseload.md):

| Patient | Contact in March | Scale in March | Active? |
|---|---|---|---|
| P1 | Phone, 10 Mar | PHQ-9, 10 Mar | Yes |
| P2 | Initial assessment 12 Mar; video 26 Mar | PHQ-9, 12 Mar | Yes |
| P3 | Video, 17 Mar | PHQ-9, 17 Mar | Yes |
| P4 | None | None | **No** |
| P6 | In person, 20 Mar | PCL-5, 20 Mar | Yes |
| P7 | Phone, 24 Mar | PHQ-9, 24 Mar | Yes |
| P8 | Video, 6 Mar | PHQ-9, 6 Mar | Yes |
| P9 | Phone, 14 Mar | PHQ-9, 14 Mar | Yes |

**Metric 5: 7 of 8, 87.5%.** P4 counts against the rate in the month of their inactivity
discharge, because they were still enrolled for the first ten days of March.

The [contacts and reviews](../concepts/contacts-and-reviews.md#worked-example) page has a
second example with the harder cases: a scale with no contact, a contact with no scale,
and a portal message.

## Where the data lives

Contacts from the registry's contact log, or BHCM and telephone encounters in the EHR.
Scales from the registry's scale table, or questionnaires and flowsheets in the EHR. See
[contacts and reviews](../concepts/contacts-and-reviews.md#where-the-data-lives).

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting outreach attempts or scheduling calls as contacts | Overstated |
| Counting patients with a contact but no scale, or a scale but no contact | Overstated |
| Counting the psychiatric case review as a contact | Overstated |
| Leaving disengaged patients enrolled | Understated |
| Running the report before late notes are in | Understated |

## For automation

Reads [`cocm_episode`](../../data-contract.md#t3-cocm_episode--one-row-per-enrollment),
[`coverage`](../../data-contract.md#t2-coverage),
[`contact`](../../data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient)
(`contact_kind = treatment`) and
[`scale_result`](../../data-contract.md#t5-scale_result--one-row-per-completed-scored-administration).
