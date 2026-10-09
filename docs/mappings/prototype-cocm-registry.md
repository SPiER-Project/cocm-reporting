# Mapping: a prototype CoCM registry → data contract

This page maps the data model of a prototype CoCM registry (Next.js + Prisma +
PostgreSQL) to the [data contract](../data-contract.md). It is the first registry mapping
(way 2 in [`filling-the-tables.md`](../filling-the-tables.md)), and also a worked example
of what a mapping has to settle.

**Mapped against:** the registry's Prisma schema as of 2026-03. No export code exists yet.

## Summary

The registry covers the CoCM half of the contract (T3–T6), with one gap in each table. It
has nothing for the EHR half: coverage (T2) and practice visits (T7) must come from the
practice-management system, which is the two-source pattern every site will have.

| Metric | From the registry alone? |
|---|---|
| 1 Total enrollment | Yes, once the [status rules](#episode-status) are settled |
| 2–4 | No: they need coverage (T2) |
| 5 Contact rate | Needs coverage, and [T4's gap](#t4-contact--patientcontact) overstates it |
| 6–8 | Needs coverage; only patients whose primary scale is PHQ-9 or GAD-7 |
| 9–10 | No: EHR |
| 11 | No: attested |

## T1 `patient` ← `Patient`

| Contract | Registry | Notes |
|---|---|---|
| `patient_id` | keyed hash of `Patient.mrn` | Not `Patient.id`, which is an internal id the EHR never sees; the two sources would never join (Q-T3) |
| `birth_date` | `dateOfBirth` | Only metric 9 uses it, and metric 9's patients come from the EHR |

## T2 `coverage` ← nothing usable

`Patient.insurance` is one JSON object (`payerId`, `memberId`, `planName`, `groupNumber`).
It has no dates, so the first-of-month rule (D-07) cannot be applied; no payer category,
so Medicaid can only be guessed from `planName`; and no history. **Coverage comes from
the practice-management system.**

## T3 `cocm_episode` ← `Episode`

| Contract | Registry | Notes |
|---|---|---|
| `episode_id`, `patient_id` | `id`, `patientId` | |
| `enrollment_date` | `startDate` | Entered by the user at enrollment. Nothing says it is the initial assessment date rather than the referral date (D-03) |
| `enrollment_source` | `registry` | Constant |
| `primary_condition` | the `diagnoses` entry with `isPrimary`, by ICD-10 range | F32, F33 → `depression`; F41 → `anxiety`; F43.1 → `ptsd`; F90 → `adhd`; else `other`. **Gap:** the schema allows zero or several primary entries; both are extraction errors |
| `primary_scale` | — | **Gap.** Derived from `primary_condition` by the D-13 default mapping. The registry stores only PHQ-9 and GAD-7, so PTSD and ADHD episodes have no scale |
| `diagnosis_date` | — | |
| `discharge_date` | `endDate` | **Gap:** optional even on `FINISHED`. Do not fall back to `updatedAt` or the audit log: those are documentation dates, which is the backdating error in D-04 |
| `discharge_reason` | `dischargeReason` | Free text; needs a lookup to the contract's list, else `other` |

### Episode status

| `status` | Contract meaning |
|---|---|
| `PLANNED`, `WAITLIST` | Not enrolled; these are referral states (D-02). Not extracted |
| `ACTIVE`, `ONHOLD` | Enrolled. On hold still counts in the denominators until discharged |
| `FINISHED` | Discharged on `endDate` |
| `CANCELLED` | **Depends on the prior status.** From `PLANNED` or `WAITLIST`: never enrolled, not extracted. From `ACTIVE` or `ONHOLD`: a discharge. Only the audit log records which |

## T4 `contact` ← `PatientContact`

The weakest mapping.

| Contract | Registry | Notes |
|---|---|---|
| `contact_id`, `patient_id`, `contact_date` | `id`, `patientId`, `date` | No episode link; contacts are attributed to an episode by date |
| `modality` | `type` | `PHONE`, `VIDEO`, `IN_PERSON` map directly |
| `contact_kind` | `type` and `successful` | `PORTAL_MESSAGE`, `EMAIL` → `message`. `successful = false` → `outreach_attempt`. **Gap:** `successful = true` means the patient was reached, not that treatment was delivered; a scheduling call looks the same as a session |
| `staff_role` | — | **Gap:** no author. Extracted as `bhcm`, and disclosed |
| `with_caregiver` | — | |

A stricter rule for `treatment`, closer to D-14's "corroborating documentation": a
reached contact counts only if a `ClinicalNote` of type `PROGRESS` or `PHONE` exists for
that patient on the same day. Notes carry only `createdAt` (entry time), so a note written
the next morning misses. Which rule a site uses goes in the disclosures.

## T5 `scale_result` ← `AssessmentScore`

The cleanest mapping.

| Contract | Registry | Notes |
|---|---|---|
| `result_id`, `patient_id` | `id`, `patientId` | |
| `administered_date` | `administeredAt` | Stored in UTC. **Convert to the site's time zone before taking the date** (D-01), or an evening score on the last day of the month lands in the next month |
| `instrument` | `instrumentType` | `PHQ9` → `phq9`, `GAD7` → `gad7`, `PHQ2` → `phq2`. `GAD2` and `CSSRS` are not NYS instruments and are not extracted |
| `total_score` | `totalScore` | |
| `context` / `context_basis` | `monitoring` / `registry` | Every score belongs to an episode. **Except** a score dated before its episode's `startDate`: that is a screening score entered into the episode, extracted as `screening`, so it cannot become the baseline (D-12) |
| `administered_by_role` | `performer.role` | `BHCM` → `bhcm`, `PCP` → `medical_provider`, else `other`. The performer is whoever "administered or entered" it, so this is weak evidence |
| `loinc` | `loincCode` | |

## T6 `psych_review` ← `Consultation`

| Contract | Registry | Notes |
|---|---|---|
| `review_id`, `patient_id`, `review_date` | `id`, `patientId`, `consultationDate` | One row per patient, the shape the contract requires |
| `recommendation_documented` | `recommendations` is non-empty after trimming | Required in the schema, but an empty string passes |
| `recommendation_to` | — | Not captured |

Not sources for T6: `TimeEntry` with `SCR_PARTICIPATION` (meeting attendance, the error in
D-17), and `ClinicalNote` of type `SCR` (one note per caseload review, not per patient).

## T7 `practice_visit`, T8 `site_month`

T7 comes from the EHR. The registry stores no FTE for T8; `TimeEntry` minutes per BHCM per
month could cross-check an attested figure, but logged time is not scheduled effort.

## Changes to the registry that would close the gaps

1. `PatientContact`: a performer, a purpose (treatment / outreach / scheduling), and an
   episode link. This is the one that fixes metric 5.
2. `Episode`: a `primaryScale`; `endDate` required on `FINISHED`; `dischargeReason` as an
   enum.
3. A coverage history table with a payer category, if the registry should report
   metrics 2–8 without the practice-management system.
4. `Consultation.recommendationTo`.
5. PCL-5, SMFQ, SCARED, PSC-17 and Vanderbilt, for pediatric or PTSD caseloads.
