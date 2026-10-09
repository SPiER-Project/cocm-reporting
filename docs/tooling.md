# Tooling plan

The secondary goal: electronic means of capturing the data, so sites don't have to
assemble it by hand. This page is for the people building the tools. Clinic-facing
collection guidance is in [`collecting/`](collecting/overview.md).

**Status:** the [calculator](#the-calculator) is built and tested against the guide's
worked examples. The other ways in are options for discussion.

## The pieces

- **The [data contract](reference/data-contract.md):** the eight tables every route produces.
- **The rules file, [`rules/calls.toml`](../rules/calls.toml):** every value the guide's
  calls set. The calculator takes its settings from it, so changing a call there changes
  the tool and the docs together.
- **The calculator:** reads the eight tables and the rules file, and returns the eleven
  numbers in the REDCap form's shape. It also returns a patient-level list of who fell out of each numerator
  and why; that list stays at the site.
- **Ways in:** the [workbook](collecting/workbook.md), registry mappings, EHR report
  recipes, and FHIR. Each fills some or all of the tables.

## The calculator

[`calculator/`](../calculator/) computes the eleven metrics from a directory of
data-contract CSVs, following [`rules/calls.toml`](../rules/calls.toml):

```bash
python3 -m calculator tests/fixtures/example-caseload --month 2025-03
```

Add `--json results.json` to also write the full results. The output includes:
- the eleven numbers;
- the disclosures for NYS;
- warnings, such as a run before the 15th or calls still needing approval;
- for each metric, the patients who fell out of the numerator and why. This list
  identifies patients by pseudonymous id and stays at the site.

**How it's built.** It uses the Python standard library only. The core works on text in
memory, not files, so the same code can run in a browser through Pyodide: a site could
drop its CSVs into a web page, and nothing would leave its machine. Each step of the
calculation names the call it implements.

**How it's tested.** `python3 -m unittest discover tests` runs it on every fixture in
[`tests/fixtures/`](../tests/fixtures/) and compares the output with `expected.toml`,
metric by metric and patient by patient. It also tests the edge of each rule: the
90th day without contact, exactly half the baseline, a 12th birthday on the visit date,
an empty denominator. CI runs the tests on every pull request.

**In the browser.** The same calculator runs in a web page:
[https://spier-project.github.io/nys-omh-cocm-caseload-reporting/](https://spier-project.github.io/nys-omh-cocm-caseload-reporting/).
- A site adds its CSV files and gets the numbers. The files are read in the browser and
  never uploaded.
- The page is one self-contained file, [`web/index.html`](../web/index.html), built from
  [`web/template.html`](../web/template.html) by `python3 scripts/build_web.py`. The
  build inlines the calculator's source, the rules file and the example caseload.
- Only Pyodide, the Python engine, comes from a CDN.
- The file works from GitHub Pages, from a download, or from a shared drive.
- Pages republishes it whenever `main` changes. CI fails if the built file is out of
  date with its sources.

**Not yet built:**
- the REDCap output format, which waits on NYS's form (Q-T5);
- the pseudonymization tool (Q-T3).

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

1. **The workbook.** Built: [the workbook route](collecting/workbook.md). It's generated
   from the data contract by `scripts/build_workbook.py`, and the calculator (command
   line and browser) reads it directly.
2. **Registry mappings**, starting with whichever registries a survey of NYS sites says
   are most common. They cover metrics 1–8 for most sites.
3. **EHR report recipes** for metrics 9–10 and coverage, starting with the most common
   EHRs among NYS CoCM sites, written against [the generic specification](collecting/ehrs/README.md).
4. **FHIR**, as an alternative to step 3, when a site asks for it.

The survey (which registries and which EHRs NYS's CoCM sites use) is the one piece of
information that would most change this order.
