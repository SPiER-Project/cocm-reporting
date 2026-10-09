# Proposal: restructure the docs as a clinic's reporting guide

**Status:** agreed; Markdown in the repo. Steps 1 to 4 are done. The calls table below has
moved to [`reference/our-calls.md`](reference/our-calls.md), which is now the version to
review and edit.

## The goal this serves

1. **First:** opinionated documentation that tells a New York clinic how to report the
   eleven CoCM metrics NYS OMH asks for, and how to get each fact out of the systems
   it actually has.
2. **Later:** electronic means of capturing that data automatically.

The current docs grew the other way round. The most finished pieces (the data contract,
the calculator idea, the registry mapping) serve the second goal. A clinic reader has no
page that says "here is metric 5, here is who counts, here is where to find it."

## What's wrong with the current shape, for a clinic reader

- **There are no metric pages.** The draft refers to a "Section 2" of metrics that was
  never written. The definitions (D-01 … D-19) are there; the eleven metrics built on
  them are not.
- **The current answer is spread over three documents.** The draft keeps its known
  errors on purpose; the corrections are in the review notes; the policy questions are
  in open-questions. To learn what to do, a reader has to merge all three.
- **It defers where it should decide.** "Decision needed", "calculator setting" and
  "pending" are the right posture for tooling. Guidance has to make the call, say why,
  and say what changes if NYS rules otherwise.
- **The IDs are for maintainers.** D-xx, D-xxa, R-xx, Q-xx and Q-T* make sense to the
  people revising the draft. A program lead doesn't need them.

## Principles for the new docs

1. **Lead with the metric.** Most readers arrive asking about one number.
2. **Make a call everywhere NYS is silent.** Each call is labelled so the reader knows
   how firm it is:
   - **NYS says**: from the source document.
   - **Our call**: NYS is silent or ambiguous; we decided, and say why.
   - **Needs clinical sign-off**: our call, but outside what a reporting team should
     decide alone (for example, remission thresholds for pediatric scales).
3. **One current answer per question.** The guide states the rule as it stands now.
   History lives in git and in an archived copy of draft v0.1, not in the reader's path.
4. **Two readers per page.** The **program lead** needs what counts and what to do
   operationally (for example, discharge inactive patients). The **report writer** needs
   where the data lives and how to pull it. Each page has a section for each.
5. **Automation sits underneath, not in front.** The data contract and mappings stay,
   as reference. Clinic pages link to them but don't depend on them.
6. **Readable names, not numbers.** Calls get slugs (`remission-timing`), not `D-16a`,
   so links and anchors explain themselves.

## Proposed layout

```
README.md                          What this is, who it's for, where to start
docs/
  guide/
    start-here.md                  The monthly cycle: what NYS asks, when to run, how to use this guide
    site-setup.md                  Settings to fix once: age floor, payer mapping, inactivity
                                   discharge, primary scale per condition. A checklist
    concepts/                      The shared definitions, rewritten as recommendations
      reporting-month.md           Reporting period, run date, restatements (D-01, D-19)
      enrollment-and-discharge.md  Enrollment, enrollment date, discharge, "enrolled this month",
                                   days in treatment (D-02 – D-06)
      medicaid.md                  Who counts as Medicaid, and on what date (D-07)
      scales-and-outcomes.md       Instruments, baseline, primary scale, improvement,
                                   remission (D-11 – D-13, D-15, D-16)
      contacts-and-reviews.md      Clinical contact; psychiatric case review (D-14, D-17)
      screening.md                 Practice visits, who should be screened, screening vs.
                                   monitoring (D-08 – D-10)
      bhcm-fte.md                  (D-18)
    metrics/
      01-total-enrollment.md
      …                            One page per NYS metric, same template
      11-bhcm-staffing.md
  collecting/                      How to get the facts out of your systems
    overview.md                    Two sources (registry + EHR), the shared patient id,
                                   what lives where (from filling-the-tables.md)
    workbook.md                    The spreadsheet route
    registries/
      prototype-cocm-registry.md   (moved from mappings/)
    ehrs/                          One recipe per EHR, as they're written
  reference/
    nys-source/
      nys-omh-cocm-metrics-2025.pdf
      nys-omh-cocm-metrics-2025.md A faithful text transcription, so pages can link to a line
    our-calls.md                   Every place we go beyond or interpret NYS: the call, why,
                                   firmness, what changes if NYS rules otherwise
    instruments.md                 Scales, elevated-baseline and remission thresholds,
                                   LOINC codes (each one checked against LOINC)
    data-contract.md               The eight tables (unchanged; serves automation)
  open-questions.md                Only what's still open, including tooling questions
  archive/
    reporting-spec-draft-v0.1.md   Frozen as circulated
    review-notes-v0.1.md           Frozen; each note says where it was applied
```

### The metric page template

1. **What NYS asks.** The source text, quoted, with a link to the transcription.
2. **The rule.** Plain-language numerator and denominator, step by step, with the
   concepts linked. Every call is labelled (**NYS says** / **Our call** / **Needs
   clinical sign-off**).
3. **Worked example.** Five or six patients, showing who is in and who is out, and why.
4. **Where the data lives.** Registry, EHR, billing; links into `collecting/`.
5. **Common mistakes.** The errors that move this number, with what each does to it.
6. **For automation.** Which data-contract tables and columns this metric reads.

Concept pages use the same template without the worked example, unless one helps.

### What `our-calls.md` replaces

The draft's decision log, the review notes that change a measure (R-01 – R-10), and the
measure questions in open-questions (Q-01 – Q-09) collapse into one register. Editorial
notes (R-11 – R-13) are simply fixed. R-14 (LOINC codes) becomes the task of verifying
every code in `instruments.md`.

## The calls the guide would make

Restructuring forces these, because a metric page can't be written without an answer.
Here are proposed answers to react to. Most follow from the NYS text more closely than
the draft did.

| Question | Proposed call | Firmness | Why |
|---|---|---|---|
| Metric 7: all payers or Medicaid? | Medicaid | Our call | The NYS description says "patients", but its numerator and denominator both say Medicaid patients. *New; not in the review notes.* |
| Remission timing (Q-02) | A qualifying score on the primary scale **in the month** | Our call | NYS says "achieved remission criteria during this month." No score this month, no remission. |
| Remission and elevated baseline (Q-03) | Required | Our call | Otherwise a patient who enrolls with a PHQ-9 of 4 is in remission on day one. Matches the improvement rule. |
| Improvement with no score this month (D-15a) | Carry forward the most recent score in the episode | Our call | Improvement, unlike remission, isn't worded "this month". Keep the draft's call, but say so. |
| Metric 8 denominator (Q-05) | Only patients with an elevated baseline | Our call | It is defined as "did not meet improvement criteria", and improvement is only assessed with an elevated baseline (Appendix A). |
| Metric 9 denominator (Q-01) | Patients with a visit with a medical provider (the draft's qualifying visit), aged 12+ | Our call | NYS defers to "practice criteria for universal depression screen". Screening happens at medical visits, and lab and nurse visits inflate the count. Publish this as the recommended practice criteria. |
| Monitoring PHQ counts as screened (Q-04) | Yes | Our call | NYS numerator: "received a PHQ-2 or 9 … in the last 12 months." Excluding CoCM patients' PHQs penalizes the practices doing the most screening. |
| "Initial PHQ-9" in metric 10 (Q-07) | The patient's first PHQ-9 in the 12 months ending with this one | Our call | "First ever" can't be known from most systems; "first this month" counts repeat PHQ-9s. |
| "Diagnosed and enrolled" in metric 3 (Q-06) | Enrollment date in the month; enrollment requires a qualifying diagnosis | Our call | No system records a separate diagnosis date reliably. |
| 70 days (R-07) | 70 or more days elapsed since the enrollment date | Our call | Fixes the off-by-one; matches "at least 10 weeks". |
| Weeks in metric 4 (R-08) | Average the days, then divide by 7; one decimal | Our call | Simplest rule that two analysts will compute the same way. |
| Paired forms: SCARED, SMFQ, Vanderbilt (Q-08, Q-09) | Baseline per form; the patient meets criteria if either form does | NYS says (for improvement) | Appendix A says "and/or" and "OR". The Vanderbilt remission rule stays **needs clinical sign-off**. |
| Pediatric thresholds; non-PHQ/GAD remission | Keep the draft's proposals | Needs clinical sign-off | Not a reporting decision. |

The rest of the draft's decision log stays as proposed. Those calls include:

- the overlap rule for "enrolled this month";
- Medicaid as of the first of the month, counting dual eligibles and excluding Child Health Plus (CHP) and the Essential Plan;
- discharge after 90 days without contact;
- the 14-day baseline window;
- BHCM FTE counting BHCMs only;
- running the report 15 days after month end.

## How to get there

Each step is a reviewable PR.

1. **Skeleton and register.**
   - Create the layout.
   - Move the draft and review notes to `archive/`.
   - Write `our-calls.md` from the table above once you've reacted to it.
   - Transcribe the NYS PDF.
2. **Concepts.** Rewrite D-01 – D-19 as the seven concept pages, applying the calls.
3. **Metrics.** The eleven metric pages, with worked examples. These are the core of the guide.
4. **Collecting.** Move `filling-the-tables.md` and the mapping, then add the workbook page.
   Done. The builder-facing parts of `filling-the-tables.md` (costs to us, FHIR coverage,
   what to build first) went to a new [`tooling.md`](tooling.md), and `collecting/ehrs/`
   starts with a vendor-neutral specification of the EHR reports.
5. **Reference.** Write `instruments.md` with verified LOINC codes. Update the data
   contract wherever a call changed what's needed. Q-04 and Q-07 shrink what `context`
   must carry.
6. **README.** Rewrite it around the two readers and the "start here" path.

**Data-contract changes found while writing the concept pages,** for step 5:

- `scale_result.instrument` needs `phq_a`, or a rule that the PHQ-A is extracted as `phq9`.
- `scale_result.context` and `context_basis` are no longer read by the screening metrics,
  and the baseline only needs the date. They could become optional, or go.
- The extraction lookbacks need stating: 12 months of PHQ-2 and PHQ-9 for metric 9, 365
  days before the month's earliest PHQ-9 for metric 10, and 90 days of contacts for the
  inactivity rule.
- Who applies the inactivity discharge: the site in `cocm_episode`, or the calculator from
  `contact`. The concept page assumes either can.
- `psych_review.recommendation_to` isn't used by any rule.

Automation work (the calculator, the workbook file, connectors) waits until step 3,
because the metric pages are its specification.

## Decisions for you

1. **The calls.** Accept, change or defer each row in the table above.
2. **The archive.** Keep draft v0.1 and the review notes in the repo, or rely on git
   history alone? Proposed: keep them; it's cheap and shows the provenance of each call.
3. **Who the guide speaks for.** "Our call" needs an "our". Is it SPiER, HTD, a named
   working group, or unattributed?
4. **Where it's read.** In the repo as Markdown, or published as a site (GitHub Pages or
   similar)? It doesn't change the structure, but it changes how links and the PDF
   transcription are done.
