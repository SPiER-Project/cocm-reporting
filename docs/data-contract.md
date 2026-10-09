# Data contract

Every site produces the same eight tables, however it produces them. One calculator
reads them and computes the eleven NYS metrics. How a site fills each table is in
[`collecting/overview.md`](collecting/overview.md).

**Status:** sketch. Column names and code lists will change; no schema file exists yet.

## Rules

1. **Every column is a fact the site already records.** Baseline, "enrolled this month",
   days in treatment, improvement and the Medicaid flag are **derived** concepts. They are
   computed once, by the calculator, and never extracted. Those are the places where two
   sites' report writers would disagree.
2. **Rows are events, not summaries.** The calculator works out each month's status.
3. **Raw categories stay raw where a decision is pending.** Payer type is not collapsed
   to Medicaid yes/no; visit provider type is not collapsed to "qualifying". When NYS
   rules, a calculator setting changes and no site rewrites its extract.
4. **No direct identifiers.** `patient_id` is a stable pseudonym, the same in every
   table and every source system (see Q-T3 in [`open-questions.md`](open-questions.md)).

## The tables

### T1. `patient`

| Column | Type | Req | Notes |
|---|---|---|---|
| `patient_id` | string | ✓ | Stable pseudonym, not the MRN |
| `birth_date` | date | ✓ | For age at visit (D-09). Used only by metric 9 |

### T2. `coverage`

| Column | Type | Req | Notes |
|---|---|---|---|
| `patient_id` | string | ✓ | |
| `payer_category` | enum | ✓ | `medicaid_ffs` · `medicaid_managed_care` · `dual_medicare_medicaid` · `child_health_plus` · `essential_plan` · `medicare` · `commercial` · `self_pay` · `other` |
| `start_date` | date | ✓ | |
| `end_date` | date | | Blank means still active |
| `plan_name` | string | | Optional; lets a reviewer spot a managed-care plan miscoded as commercial |

Extract every coverage period that overlaps the reporting month. Which categories count
as Medicaid, and on what date (D-07a), is a calculator setting.

### T3. `cocm_episode` — one row per enrollment

| Column | Type | Req | Notes |
|---|---|---|---|
| `episode_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `enrollment_date` | date | ✓ | Date of the initial BHCM assessment (D-03), not the referral |
| `enrollment_source` | enum | ✓ | `registry` · `ehr_structured` · `billing_inferred` (the D-02a fallback, disclosed automatically) |
| `primary_condition` | enum | ✓ | `depression` · `anxiety` · `ptsd` · `adhd` · `general_pediatric` · `other` |
| `primary_scale` | enum | ✓ | Chosen at enrollment, from the instrument list in T5 (D-13) |
| `diagnosis_date` | date | | Only if metric 3's "diagnosed" means more than enrolled (Q-06) |
| `discharge_date` | date | | Blank means enrolled |
| `discharge_reason` | enum | | `graduated` · `lost_to_follow_up` · `administrative_inactivity` · `withdrew` · `transferred` · `died` · `other` |

Extract every episode that overlaps the reporting month. A re-enrollment is a new row,
so a baseline never carries across episodes.

### T4. `contact` — one row per BHCM or team interaction with the patient

| Column | Type | Req | Notes |
|---|---|---|---|
| `contact_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `contact_date` | date | ✓ | Date of service, not of note signature (D-01) |
| `staff_role` | enum | ✓ | `bhcm` · `other_cocm_clinician` · `psychiatric_consultant` · `other` |
| `contact_kind` | enum | ✓ | `treatment` · `outreach_attempt` · `scheduling` · `no_show` · `message` |
| `modality` | enum | | `in_person` · `video` · `phone`. Required unless `contact_kind` is `message` |
| `with_caregiver` | bool | | Pediatric caregiver sessions |

Extract the attempts and messages too. Only `treatment` counts toward metric 5, but the full log
shows a caseload that is mostly unanswered outreach, and it is the evidence for the
D-04a inactivity rule. Psychiatric case reviews go in T6, not here.

### T5. `scale_result` — one row per completed, scored administration

| Column | Type | Req | Notes |
|---|---|---|---|
| `result_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `administered_date` | date | ✓ | |
| `instrument` | enum | ✓ | `phq2` · `phq9` · `gad7` · `pcl5` · `smfq_child` · `smfq_parent` · `scared_child` · `scared_parent` · `psc17` · `vanderbilt_parent` · `vanderbilt_teacher` |
| `total_score` | int | ✓ | No score, no row: a partial or unscored form is excluded at extraction (D-11) |
| `vanderbilt_symptom_count` | int | | Vanderbilt only: items rated 2 or 3 (Q-08) |
| `context` | enum | ✓ | `screening` · `monitoring` · `unknown` |
| `context_basis` | enum | ✓ | `registry` · `department` · `administering_role` · `site_rule` — how `context` was decided |
| `administered_by_role` | enum | | `bhcm` · `medical_provider` · `nursing_ma` · `self_report` · `other` |
| `loinc` | string | | Optional |

This is the one table both halves of the report share: monitoring rows drive metrics
5–8, screening rows drive metrics 9–10.

`context` is required because it cannot be reliably reconstructed later (D-10). A site
with a registry gets it for free. Other sites state their rule in `context_basis`, and
the submission discloses it.

The lookback is longer than the month: monitoring results from each open episode's
`enrollment_date` (the baseline lives there), and screening results for the 12 months
before the reporting month ends (metric 9's numerator).

### T6. `psych_review` — one row per patient discussed

| Column | Type | Req | Notes |
|---|---|---|---|
| `review_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `review_date` | date | ✓ | |
| `recommendation_documented` | bool | ✓ | Only `true` counts (D-17); "continue current treatment" is a recommendation |
| `recommendation_to` | enum | | `pcp` · `bhcm` · `both` |

One row per patient discussed, never one per meeting. That shape is what stops "the
consultant attended the caseload review" from counting as a review of every patient.

### T7. `practice_visit` — the denominator for metric 9

| Column | Type | Req | Notes |
|---|---|---|---|
| `visit_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `visit_date` | date | ✓ | |
| `provider_category` | enum | ✓ | `primary_care` · `other_medical` · `behavioral_health` · `nursing_only` · `ancillary` |
| `billing_codes` | string[] | | CPT/HCPCS as billed. The calculator applies the D-08 list if NYS adopts it |
| `modality` | enum | ✓ | `in_person` · `video` · `phone` |

Every visit in the month, all payers. Keeping every visit is what lets Q-01 ("for any
reason" vs. qualifying visits) be a setting.

### T8. `site_month` — one row per submission

| Column | Type | Req | Notes |
|---|---|---|---|
| `site_id` | string | ✓ | NYS-assigned |
| `reporting_month` | YYYY-MM | ✓ | |
| `bhcm_fte` | decimal | ✓ | Attested (metric 11, D-18) |
| `screening_age_floor` | int | ✓ | Until D-09a is settled |
| `extract_run_date` | date | ✓ | The calculator warns if this is earlier than the D-19 lag |
| `source_system` | string | ✓ | e.g. `registry`, `epic`, `ecw`, `spreadsheet` |
| `notes` | text | | Sent to NYS |

The calculator adds the disclosures to this row: enrollment sources used, how scale
context was decided, and the share of `unknown` contexts.

## Which tables each metric reads

| Metric | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|---|---|---|---|---|---|---|---|---|
| 1 Total enrollment | | | ● | | | | | ● |
| 2 Medicaid enrollment | | ● | ● | | | | | |
| 3 Newly enrolled | | ● | ● | | | | | |
| 4 Duration of treatment | | ● | ● | | | | | |
| 5 Contact rate | | ● | ● | ● | monitoring | | | |
| 6 Improvement | | ● | ● | | monitoring | | | |
| 7 Remission | | ● | ● | | monitoring | | | |
| 8 Psychiatric consultation | | ● | ● | | monitoring | ● | | |
| 9 Screening rate | ● | | | | screening | | ● | ● |
| 10 Screening yield | | | | | screening | | | |
| 11 BHCM FTE | | | | | | | | ● |
