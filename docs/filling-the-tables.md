# Filling the tables

The [data contract](data-contract.md) says *what* a site produces. This page is about
*how*: where each table's facts live, and the ways a site can get them into the
contract's shape. It ends with the decision we need to make about what to build first.

**Status:** options for discussion. Nothing here is built.

## Where each table's facts live

The NYS document itself says metrics 9–10 are "not tracked in your CoCM registry". So
almost every site has **at least two sources**: the CoCM registry (or whatever stands in
for one) and the EHR or practice-management system.

| Table | Usual source | Notes |
|---|---|---|
| T1 `patient` | EHR / practice management | |
| T2 `coverage` | Practice management, billing | Registries rarely carry payer, and almost never its history |
| T3 `cocm_episode` | **Registry**; else an EHR program-enrollment record | The fallback is billing codes (D-02a), disclosed |
| T4 `contact` | **Registry** contact log; else BHCM encounters in the EHR | Outreach attempts are often only in the registry |
| T5 `scale_result`, monitoring | **Registry**; else EHR questionnaires or flowsheets | |
| T5 `scale_result`, screening | EHR (primary care questionnaires or flowsheets) | Never in the registry |
| T6 `psych_review` | **Registry**; else consultant notes in the EHR | Hardest to get from an EHR; often only a note, with no structured field |
| T7 `practice_visit` | EHR / practice management | |
| T8 `site_month` | Typed in by the program lead | |

## The ways in

All four produce the same eight tables. A site can mix them: a registry export for
T3–T6, plus an EHR report for T1, T2, T5-screening and T7.

### 1. Workbook

A spreadsheet with one tab per table, dropdowns for every code list, and a validation
tab that flags missing required columns and impossible dates.

- **For:** sites whose "registry" is already a spreadsheet, and sites without a report
  writer.
- **Cost to the site:** manual entry or copy-paste each month. T7 (every visit in the
  month) is the hard tab, and usually needs one report from the billing system.
- **Cost to us:** low. The workbook is the contract with formatting.

### 2. Registry export mappings

A column mapping from a registry's own export to T3–T6, for each registry sites
actually use. That includes the free registry spreadsheet many CoCM programs start from,
and the commercial measurement-based-care platforms.

- **For:** sites with a registry. Most CoCM programs keep one, because the model
  requires a caseload registry.
- **Cost to the site:** run the registry's existing export.
- **Cost to us:** one mapping per registry product, kept current as products change.
  We need a survey of which registries NYS sites use before choosing.

### 3. EHR report recipes

For each major EHR, a written query or report specification producing T1, T2, T5 and
T7 (and T3–T6 for sites with no registry). It is written for that site's report writer,
not run by us.

- **For:** sites with a report writer or analyst.
- **Cost to the site:** a one-time build by their analyst, then a monthly run.
- **Cost to us:** knowing each EHR's data model well enough to write a recipe that is
  right, not just plausible. The screening-vs-monitoring context (D-10) is where recipes
  will differ most.

### 4. FHIR

Pull from the EHR's standard FHIR API, using a bulk export of the patient population.

| Table | FHIR coverage |
|---|---|
| T1, T2, T7 | Good: `Patient`, `Coverage`, `Encounter` are standard and widely exposed |
| T5 screening | Partial: the PHQ-9 total is commonly exposed as an `Observation` with a LOINC code. Context is not, and must be inferred from the encounter |
| T3, T4, T6 | Poor: CoCM enrollment, outreach attempts and psychiatric case review have no standard representation that EHRs expose |

- **For:** sites with FHIR access and someone to run it. Few community practices have
  both today.
- **Conclusion:** FHIR can replace the EHR report recipe (way 3) for T1, T2, T5-screening
  and T7. It does not replace the registry (way 2) for the CoCM tables.

## What every way in shares

- **One pseudonym.** The registry and the EHR must produce the same `patient_id` for the
  same patient, or the two halves never join. The simplest rule is a keyed hash of the
  MRN, using a secret the site keeps. It needs a small tool both exports run through
  (Q-T3).
- **One calculator.** It reads the eight tables, whatever produced them, and returns the
  eleven numbers in the REDCap form's shape, plus a patient-level list of who fell out of
  each numerator and why. The list stays at the site.
- **Disclosures.** Each way in records how it filled the judgement columns
  (`enrollment_source`, `context_basis`), and the submission carries them to NYS.

## What to build first

This is Q-T1 in [`open-questions.md`](open-questions.md). A proposal to react to:

1. **The workbook and the calculator, together.** The workbook is the contract made
   usable, it serves every site on day one, and it gives the calculator real input to be
   tested against.
2. **Registry mappings**, starting with whichever registries a quick survey of NYS
   sites says are most common. This covers the CoCM half (metrics 1–8) for most sites.
3. **EHR report recipes** for the screening half (metrics 9–10), starting with the most
   common EHRs among NYS CoCM sites.
4. **FHIR**, as an alternative to step 3, when a site asks for it.

The survey in step 2 (which registries and which EHRs NYS's CoCM sites use) is the one
piece of information that would most change this order.
