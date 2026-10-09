# Collaborative Care (CoCM) Caseload Reporting Framework for the New York State Office of Mental Health

A specification and tooling for the monthly CoCM caseload metrics that practices report
to the New York State Office of Mental Health (OMH). The aim is for practices with very
different technical capabilities to report them the same way: from a spreadsheet
registry to an EHR with a reporting team.

**Status:** documents only. Nothing is built yet, and the measure definitions have open
decisions.

## The approach

**Sites extract facts; the logic is implemented once.**

- Every site produces the same eight tables: patients, coverage, CoCM episodes,
  contacts, scale results, psychiatric reviews, practice visits, and one row of
  site-month facts. Each column is something the site already records.
- One calculator reads the tables and produces the eleven NYS numbers. Baselines,
  "enrolled this month", improvement and remission are computed there, so no site
  re-implements them, and a decision NYS makes later changes one setting.
- Sites can fill the tables several ways: a workbook, a registry export, an EHR report,
  or a FHIR export.

## What's here

| Path | What it is |
|---|---|
| [`docs/guide/`](docs/guide/start-here.md) | The guide: one page per metric and per shared concept. **Start here.** Being written |
| [`docs/reference/our-calls.md`](docs/reference/our-calls.md) | Every place the guide interprets NYS or goes beyond it: the call, why, and how firm it is |
| [`docs/reference/nys-source/`](docs/reference/nys-source/) | The NYS OMH metrics document (2025), as a PDF and as a linkable transcription |
| [`docs/reference/data-contract.md`](docs/reference/data-contract.md) | The eight tables every route produces, for the tooling |
| [`docs/reference/instruments.md`](docs/reference/instruments.md) | The symptom scales: scoring, thresholds and their sources, and verified LOINC codes |
| [`docs/collecting/`](docs/collecting/overview.md) | Where each fact lives in a clinic's systems, the routes for getting it out, and one page per registry or EHR |
| [`docs/tooling.md`](docs/tooling.md) | The plan for electronic capture: the ways in, what each costs, what to build first |
| [`docs/open-questions.md`](docs/open-questions.md) | What's still open: for NYS, for a clinician, to verify, and about the tooling |
| [`docs/archive/`](docs/archive/) | Draft v0.1 and its review notes, frozen. Superseded by the guide and `our-calls.md` |
