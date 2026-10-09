# Collaborative Care (CoCM) Caseload Reporting Framework for the New York State Office of Mental Health

How a New York clinic reports the eleven monthly CoCM caseload metrics that the New York
State Office of Mental Health (OMH) asks for, and how to get each fact out of the
systems it has: a spreadsheet registry, a registry product, or the EHR alone.

The guide is opinionated. The [NYS document](docs/reference/nys-source/nys-omh-cocm-metrics-2025.md)
leaves much undefined:
- who counts as enrolled;
- what remission means;
- which visits should be followed by a depression screen.

Where it's silent or ambiguous, the guide makes a call, says why, and says how firm it is.
Two clinics that follow it should report the same numbers from the same patients.

**Status:** the guide is written. Every one of its calls still **needs approval**, so treat
the guide as provisional. The project has adopted the more mechanical calls; the rest
are proposed, and some need a clinician's sign-off. The
[open questions](docs/open-questions.md) list what's outstanding. Nothing for automated
capture is built yet.

## Start here

| If you are… | Read |
|---|---|
| A **CoCM program lead** | [Start here](docs/guide/start-here.md), then the [metric pages](docs/guide/start-here.md#the-metrics). Each one has a "What the program should do" section |
| A **report writer or analyst** | [Collecting the data](docs/collecting/overview.md) for your route, then the metric pages' "Where the data lives" sections |
| Checking a **number you've already reported** | The [example caseload](docs/guide/example-caseload.md), which works all eight CoCM metrics through ten patients |
| Reviewing the **guide's decisions** | [Our calls](docs/reference/our-calls.md), which lists each one with its reasoning, firmness and status |
| **Building tools** to capture the data | The [tooling plan](docs/tooling.md) and the [data contract](docs/reference/data-contract.md) |

## The metrics

| # | Metric | Population | 2025 target |
|---|---|---|---|
| 1 | [Total enrollment](docs/guide/metrics/01-total-enrollment.md) | CoCM, all payers | — |
| 2 | [Medicaid enrollment](docs/guide/metrics/02-medicaid-enrollment.md) | CoCM, Medicaid | — |
| 3 | [Newly enrolled](docs/guide/metrics/03-newly-enrolled.md) | CoCM, Medicaid | — |
| 4 | [Average duration of treatment](docs/guide/metrics/04-average-duration-of-treatment.md) | CoCM, Medicaid | — |
| 5 | [Monthly contact rate](docs/guide/metrics/05-monthly-contact-rate.md) | CoCM, Medicaid | ≥ 80% |
| 6 | [Improvement rate](docs/guide/metrics/06-improvement-rate.md) | CoCM, Medicaid | ≥ 60% |
| 7 | [Remission rate](docs/guide/metrics/07-remission-rate.md) | CoCM, Medicaid | — |
| 8 | [Psychiatric consultation rate](docs/guide/metrics/08-psychiatric-consultation-rate.md) | CoCM, Medicaid | ≥ 80% |
| 9 | [Depression screening rate](docs/guide/metrics/09-depression-screening-rate.md) | Whole practice | 85% |
| 10 | [Depression screening yield](docs/guide/metrics/10-depression-screening-yield.md) | Whole practice | — |
| 11 | [BHCM staffing](docs/guide/metrics/11-bhcm-staffing.md) | Attested | — |

## What's here

| Path | What it is |
|---|---|
| [`docs/guide/`](docs/guide/start-here.md) | The guide: a page per metric, a page per shared concept, and the example caseload |
| [`docs/collecting/`](docs/collecting/overview.md) | Where each fact lives, the three routes for getting it out, the workbook route, the EHR report specification, and one page per registry |
| [`docs/reference/our-calls.md`](docs/reference/our-calls.md) | Every call the guide makes |
| [`docs/reference/instruments.md`](docs/reference/instruments.md) | The symptom scales: scoring, thresholds with their sources, and verified LOINC codes |
| [`docs/reference/nys-source/`](docs/reference/nys-source/) | The NYS OMH metrics document (2025), as a PDF and as a linkable transcription |
| [`docs/reference/data-contract.md`](docs/reference/data-contract.md) | The eight tables every route produces, for the tooling |
| [`docs/tooling.md`](docs/tooling.md) | The plan for electronic capture: the ways in, what each costs, what to build first |
| [`docs/open-questions.md`](docs/open-questions.md) | What's still open: for NYS, for a clinician, to verify, and about the tooling |
| [`docs/archive/`](docs/archive/) | Draft v0.1 and its review notes, frozen. Each call in `our-calls.md` names what it replaces there |

## Changing the guide

- **Every interpretation of NYS is a call.** Each call has two halves:
  - its reasoning, in [`our-calls.md`](docs/reference/our-calls.md);
  - its values, in [`rules/calls.toml`](rules/calls.toml): windows, thresholds, code
    lists, and the call's status and approval.
  
  Pages state the rule and link to the call; they don't argue it.
- **Change a value only in `rules/calls.toml`, then run the sync.** The docs mark every
  place they show a rule's value, and the sync rewrites them all, including the tables of
  thresholds, codes and call statuses. The future calculator will read the same file, so
  a value can't drift between the guide and the tool.

```bash
python3 scripts/rules.py sync
```

- **Change wording in the docs as usual**, but don't edit text between
  `<!--rule:…-->` and `<!--/rule-->` or inside a `<!--rules:…-->` block; the sync
  overwrites it.
- **Each call has a firmness, a status and an approval**, all set in `rules/calls.toml`.
  - Firmness: *NYS says*, *Our call* or *Needs clinical sign-off*.
  - Status: *Proposed* or *Adopted* by the project.
  - Approval: *Needed*, *Approved* or *Confirmed by NYS*. Adopting a call doesn't approve
    it.
  
  Say who decided in the commit.
- **Keep the worked examples right.** Each example names the calls it depends on in
  [`tests/examples.toml`](tests/examples.toml). If one of those calls changes, CI marks
  the example stale until someone reworks it and records that:

```bash
python3 scripts/examples.py verify example-caseload
```

  The [example caseload](docs/guide/example-caseload.md) and the screening example are
  also test data in [`tests/fixtures/`](tests/fixtures/), in the data contract's shape.
  Change a result in `expected.toml`, not in the pages, then run
  `python3 scripts/examples.py sync`.
- **Look up codes and thresholds; don't recall them.** Cite the source on the
  [instruments](docs/reference/instruments.md) page.
- **The archive doesn't change.** Fix the guide instead.
- **Check before committing.** CI runs all three checks on every pull request:

```bash
python3 scripts/rules.py check
```

```bash
python3 scripts/examples.py check
```

```bash
python3 scripts/check_links.py
```
