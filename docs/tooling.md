# Tooling plan

The secondary goal: electronic means of capturing the data, so sites don't have to
assemble it by hand. This page is for the people building the tools. Clinic-facing
collection guidance is in [`collecting/`](collecting/overview.md).

**Status:** options for discussion. Nothing here is built.

## The pieces

- **The [data contract](reference/data-contract.md):** the eight tables every route produces.
- **The rules file, [`rules/calls.toml`](../rules/calls.toml):** every value the guide's
  calls set. The calculator takes its settings from it, so changing a call there changes
  the tool and the docs together.
- **The calculator:** reads the eight tables and the rules file, and returns the eleven
  numbers in the REDCap form's shape. It also returns a patient-level list of who fell out of each numerator
  and why; that list stays at the site.
- **Ways in:** the workbook, registry mappings, EHR report recipes, and FHIR. Each fills
  some or all of the tables.

## What each way in costs us

| Way in | Our cost | Notes |
|---|---|---|
| Workbook | Low: the contract with formatting, dropdowns and a validation tab | Serves every site on day one |
| Registry mappings | One mapping per registry product, kept current as products change | Needs a survey of which registries NYS sites use |
| EHR report recipes | Knowing each EHR's data model well enough to write a recipe that's right, not just plausible | Contacts and case reviews are where recipes will differ most |
| FHIR | A bulk-export client and the mapping from FHIR resources to the tables | Few community practices have both FHIR access and someone to run it |

What FHIR can cover:

| Table | FHIR coverage |
|---|---|
| Patients, coverage, practice visits | Good: `Patient`, `Coverage` and `Encounter` are standard and widely exposed |
| PHQ results | Good for the PHQ-9 total, commonly exposed as an `Observation` with a LOINC code. Under the guide's calls the screening metrics no longer need to know the context |
| Episodes, contacts, case reviews | Poor: CoCM enrollment, contact purpose and psychiatric case review have no standard representation that EHRs expose |

FHIR can replace an EHR report recipe for the EHR half of the tables. It can't replace
the registry for the CoCM half.

## What to build first

This is Q-T1 in [open questions](open-questions.md#the-tooling). A proposal to react to:

1. **The workbook and the calculator, together.** The workbook is the contract made
   usable, and it gives the calculator real input to test against. The guide's
   [example caseload](guide/example-caseload.md) is the first test case: the calculator
   must reproduce its eight results.
2. **Registry mappings**, starting with whichever registries a survey of NYS sites says
   are most common. They cover metrics 1–8 for most sites.
3. **EHR report recipes** for metrics 9–10 and coverage, starting with the most common
   EHRs among NYS CoCM sites, written against [the generic specification](collecting/ehrs/README.md).
4. **FHIR**, as an alternative to step 3, when a site asks for it.

The survey (which registries and which EHRs NYS's CoCM sites use) is the one piece of
information that would most change this order.
