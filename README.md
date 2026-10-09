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
| [`docs/source/`](docs/source/) | The NYS OMH metrics document (2025) |
| [`docs/spec/reporting-spec-draft.md`](docs/spec/reporting-spec-draft.md) | Shared definitions, draft v0.1 |
| [`docs/spec/review-notes.md`](docs/spec/review-notes.md) | Where draft v0.1 departs from the NYS document, contradicts itself, or leaves a term undefined |
| [`docs/data-contract.md`](docs/data-contract.md) | The eight tables |
| [`docs/filling-the-tables.md`](docs/filling-the-tables.md) | Where each table's facts live, the ways to fill them, and what to build first |
| [`docs/mappings/`](docs/mappings/) | One page per source system, mapping its data model to the eight tables |
| [`docs/open-questions.md`](docs/open-questions.md) | Questions raised since v0.1, about the measures and about the tooling |
