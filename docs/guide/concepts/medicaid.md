# Medicaid

Which patients are Medicaid patients for the month. Seven of the eleven metrics count
only Medicaid patients, so a payer mapping that misses a managed care plan understates
all seven.

**Used by:** metrics 2 to 8. Metrics 1, 9, 10 and 11 are all-payer; don't apply this
filter to them.

## What NYS says

Metrics 2 to 8 count "Medicaid patients". Metric 7's description says "patients enrolled
in treatment", but its numerator and denominator say Medicaid patients. NYS doesn't define
a Medicaid patient. ([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md))

## The rule

A patient is a Medicaid patient for the month if, **on the first day of the month**, they
have active New York State Medicaid coverage. *Our call:
[who counts as Medicaid](../../reference/our-calls.md#who-counts-as-medicaid).*

| Counts | Doesn't count |
|---|---|
| Medicaid fee-for-service | Child Health Plus |
| Medicaid managed care, under any plan name | Essential Plan |
| Health and Recovery Plans (HARPs), which are Medicaid managed care | Medicare only |
| Dual Medicare–Medicaid patients, including integrated plans for duals | Commercial, self-pay |
| Medicaid as secondary coverage | Medicaid applied for but not yet active |

- **Primary or secondary doesn't matter.** Most dual-eligible patients have Medicare as
  primary.
- **First of the month fixes the status for the whole month.** A patient who gains
  Medicaid on the 10th is not a Medicaid patient that month; one who loses it on the 10th
  still is.
- **Use the coverage known at the run date, and don't restate.** If Medicaid is later
  granted retroactively, earlier submitted months stay as they were
  ([reporting month](reporting-month.md)).
- **Metric 7 is a Medicaid metric** like the rest. *Our call:
  [remission is a Medicaid metric](../../reference/our-calls.md#remission-is-a-medicaid-metric).*

## What the program should do

The work is a **payer mapping**: a list of every payer and plan the practice bills, each
assigned to a category. Build it once, as part of [site setup](../site-setup.md), and add
to it when a new plan appears.

- **Map by plan, not by carrier.** One insurer often sells a Medicaid managed care plan,
  a Child Health Plus plan, an Essential Plan and commercial plans. Fidelis Care and
  Healthfirst are examples. The carrier name alone can't tell them apart; the plan or
  product can.
- **Expect Medicaid managed care to be listed under the plan's name.** Few plan names
  contain the word "Medicaid".
- **Have someone who knows the billing system review the list.** The front desk and
  billing often use different payer lists.

## Where the data lives

Coverage almost always comes from the **practice-management or billing system**, not the
registry.

- Use the coverage or insurance records with their effective and end dates. A
  "current insurance" field shows today's payer, not the first of the reporting month.
- The payer or financial class field is a starting point, but check it. Managed care
  plans are often classed as commercial.
- Registries rarely hold payer, and almost never its history. The
  [prototype registry](../../mappings/prototype-cocm-registry.md#t2-coverage--nothing-usable)
  stores a single insurance record with no dates, which can't support the rule.

## Common mistakes

| Mistake | Effect |
|---|---|
| Using the payer as of the run date | Patients are reclassified after the fact; metrics 2–8 shift |
| Looking for "Medicaid" in the plan name | Managed care patients are dropped; metrics 2–8 understated |
| Classifying by carrier | Child Health Plus, Essential Plan and commercial members of a Medicaid carrier are counted as Medicaid |
| Counting only primary coverage | Dual eligibles are dropped |
| Applying the Medicaid filter to metric 1, 9, 10 or 11 | All-payer metrics understated |

## For automation

- [`coverage`](../../data-contract.md#t2-coverage) holds each coverage period with a raw
  `payer_category`. The calculator decides which categories count as Medicaid, so a change
  of rule doesn't need a new extract.
- `plan_name` is optional but worth extracting. It lets a reviewer spot a managed care
  plan coded as commercial.
