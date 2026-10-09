# Data contract

Every site produces the same eight tables, however it produces them. One calculator
reads them and computes the eleven NYS metrics, applying the rules in the
[guide](../guide/start-here.md). How a site fills each table is in
[collecting the data](../collecting/overview.md).

**Status:** sketch. Column names and code lists may still change; no schema file exists
yet. This page serves the [tooling](../tooling.md); a clinic following the guide by hand
doesn't need it.

## Rules

1. **Every column is a fact the site already records.** Baseline, "enrolled this month",
   days in treatment, improvement, remission, the inactivity discharge and the Medicaid
   flag are **derived**. The calculator computes them once, and nobody extracts them.
   Those are the places where two sites' report writers would otherwise disagree.
2. **Rows are events, not summaries.** The calculator works out each month's status.
3. **Raw categories stay raw.** Payer type isn't collapsed to Medicaid yes or no, and
   visit provider type isn't collapsed to "qualifying". The guide's
   [calls](our-calls.md) are calculator settings, so if a call changes, no site rewrites
   its extract.
4. **No direct identifiers.** `patient_id` is a stable pseudonym, the same in every
   table and every source system (see [one patient id](../collecting/overview.md#one-patient-id)).
5. **Dates are local dates of the event.** They aren't timestamps, and they aren't
   documentation dates ([reporting month](../guide/concepts/reporting-month.md)).

## The tables

### T1. `patient`

| Column | Type | Req | Notes |
|---|---|---|---|
| `patient_id` | string | ✓ | Stable pseudonym, not the MRN |
| `birth_date` | date | ✓ | For age at visit. Used only by metric 9 |

Extract every patient who appears in any other table.

### T2. `coverage`

| Column | Type | Req | Notes |
|---|---|---|---|
| `patient_id` | string | ✓ | |
| `payer_category` | enum | ✓ | `medicaid_ffs` · `medicaid_managed_care` · `dual_medicare_medicaid` · `child_health_plus` · `essential_plan` · `medicare` · `commercial` · `self_pay` · `other`. HARPs are `medicaid_managed_care` |
| `start_date` | date | ✓ | |
| `end_date` | date | | Blank means still active |
| `plan_name` | string | | Lets a reviewer spot a managed care plan miscoded as commercial |

Extract every coverage period, primary or secondary, that overlaps the reporting month.
Which categories count as Medicaid is a calculator setting
([who counts as Medicaid](our-calls.md#who-counts-as-medicaid)).

### T3. `cocm_episode` — one row per enrollment

| Column | Type | Req | Notes |
|---|---|---|---|
| `episode_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `enrollment_date` | date | ✓ | Date of the BHCM's initial assessment, not the referral ([enrollment date](our-calls.md#enrollment-date)) |
| `enrollment_source` | enum | ✓ | `registry` · `ehr_structured` · `billing_inferred`. `billing_inferred` is disclosed automatically |
| `primary_condition` | enum | ✓ | `depression` · `anxiety` · `ptsd` · `adhd` · `general_pediatric` · `other` |
| `primary_scale` | enum | ✓ | One of the T5 instruments other than `phq2` ([primary scale](our-calls.md#primary-scale)) |
| `primary_scale_source` | enum | ✓ | `recorded` · `default_mapping`. `default_mapping` is disclosed automatically |
| `diagnosis_date` | date | | Unused unless NYS says "diagnosed" in metric 3 means more than enrolled ([diagnosed and enrolled](our-calls.md#diagnosed-and-enrolled)) |
| `discharge_date` | date | | As recorded. Blank means not discharged in the source |
| `discharge_reason` | enum | | `graduated` · `lost_to_follow_up` · `administrative_inactivity` · `withdrew` · `transferred` · `died` · `other` |

Extract every episode that overlaps the reporting month, plus any episode with no
recorded discharge, however old. The calculator applies the
[inactivity discharge](our-calls.md#inactivity-discharge) from T4: an episode's effective
discharge date is the earlier of the recorded date and the last treatment contact plus
90 days. A re-enrollment is a new row, so a baseline never carries across episodes.

### T4. `contact` — one row per BHCM or team interaction with the patient

| Column | Type | Req | Notes |
|---|---|---|---|
| `contact_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `contact_date` | date | ✓ | Date of service, not of note signature |
| `staff_role` | enum | ✓ | `bhcm` · `other_cocm_clinician` · `psychiatric_consultant` · `other` · `unknown`. `unknown` is disclosed automatically |
| `contact_kind` | enum | ✓ | `treatment` · `outreach_attempt` · `scheduling` · `no_show` · `message` |
| `modality` | enum | | `in_person` · `video` · `phone`. Required unless `contact_kind` is `message` |
| `with_caregiver` | bool | | Pediatric caregiver sessions |

Extract every contact since each extracted episode's `enrollment_date`. The inactivity
rule needs the last treatment contact, however long ago it was. Only `treatment` counts as
a [clinical contact](our-calls.md#clinical-contact). Extract attempts and messages too:
the full log shows a caseload that is mostly unanswered outreach. How the site decided
`treatment` goes in T8. Psychiatric case reviews go in T6, not here.

### T5. `scale_result` — one row per completed, scored administration

| Column | Type | Req | Notes |
|---|---|---|---|
| `result_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `administered_date` | date | ✓ | |
| `instrument` | enum | ✓ | `phq2` · `phq9` · `phq_a` · `gad7` · `pcl5` · `smfq_child` · `smfq_parent` · `scared_child` · `scared_parent` · `psc17` · `vanderbilt_parent` · `vanderbilt_teacher` |
| `total_score` | int | ✓ | No score, no row: a partial or unscored form is excluded at extraction. For the Vanderbilt, the score the site uses for improvement |
| `vanderbilt_symptom_count` | int | | Vanderbilt only: symptom items rated 2 or 3, for the [remission rule](our-calls.md#remission-thresholds) |
| `administered_by_role` | enum | | `bhcm` · `medical_provider` · `nursing_ma` · `self_report` · `other`. Not used by any metric; useful for review |
| `loinc` | string | | Optional. See [instruments](instruments.md#loinc-codes) for the codes that exist |

One table for both halves of the report. Rows are selected by instrument and date, not by
purpose:

- **Metrics 5–8:** any NYS scale dated on or after the episode's enrollment date. A
  score dated before it can never be the [baseline](our-calls.md#baseline).
- **Metric 9:** any PHQ-2, PHQ-9 or PHQ-A in the 12 months ending on the last day of
  the month ([what counts as screened](our-calls.md#what-counts-as-screened)).
- **Metric 10:** any PHQ-9 or PHQ-A, with the 365 days before it
  ([initial PHQ-9](our-calls.md#initial-phq-9)).

Extract every result for the patients in T3 since their episodes' enrollment dates, and
every PHQ-2, PHQ-9 and PHQ-A for any patient in the 13 months ending on the last day of
the month.

*Changed from the first sketch:* the `context` and `context_basis` columns
(screening or monitoring) are gone. Under the guide's calls no metric reads them, and
they were the hardest columns for an EHR-only site to fill.

### T6. `psych_review` — one row per patient discussed

| Column | Type | Req | Notes |
|---|---|---|---|
| `review_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `review_date` | date | ✓ | |
| `recommendation_documented` | bool | ✓ | Only `true` counts; "continue current treatment" is a recommendation ([psychiatric case review](our-calls.md#psychiatric-case-review)) |
| `recommendation_to` | enum | | `pcp` · `bhcm` · `both`. Not used by any metric |

One row per patient discussed, never one per meeting. That shape is what stops "the
consultant attended the caseload review" from counting as a review of every patient.
Extract reviews in the 60 days ending on the last day of the month.

### T7. `practice_visit` — the denominator for metric 9

| Column | Type | Req | Notes |
|---|---|---|---|
| `visit_id` | string | ✓ | |
| `patient_id` | string | ✓ | |
| `visit_date` | date | ✓ | |
| `provider_category` | enum | ✓ | `primary_care` · `other_medical` · `behavioral_health` · `nursing_only` · `ancillary` |
| `billing_codes` | string[] | | CPT and HCPCS as billed |
| `modality` | enum | ✓ | `in_person` · `video` · `phone` |

Every visit in the month, all payers. The calculator applies the
[qualifying-visit rule](our-calls.md#who-should-be-screened), and keeping every visit
means a change to that rule is a setting, not a new extract.

### T8. `site_month` — one row per submission

| Column | Type | Req | Notes |
|---|---|---|---|
| `site_id` | string | ✓ | NYS-assigned |
| `reporting_month` | YYYY-MM | ✓ | |
| `bhcm_fte` | decimal | ✓ | Attested ([BHCM FTE](our-calls.md#bhcm-fte)) |
| `screening_age_floor` | int | ✓ | 12 under the guide; a site with a different workflow states its own |
| `treatment_contact_rule` | text | ✓ | How the extract decided `contact_kind = treatment`, for example "a signed progress note on the same day" |
| `extract_run_date` | date | ✓ | The calculator warns if this is before the 15th of the following month |
| `source_system` | string | ✓ | For example `registry`, `epic`, `ecw`, `spreadsheet` |
| `notes` | text | | Sent to NYS |

The calculator adds the automatic disclosures to this row:
- the enrollment sources used;
- the share of episodes with a defaulted primary scale;
- the share of contacts with an unknown author;
- any screening age floor other than 12.

## Which tables each metric reads

Every CoCM metric reads T4, because the inactivity discharge decides who is enrolled.

| Metric | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 |
|---|---|---|---|---|---|---|---|---|
| 1 Total enrollment | | | ● | ● | | | | ● |
| 2 Medicaid enrollment | | ● | ● | ● | | | | |
| 3 Newly enrolled | | ● | ● | ● | | | | |
| 4 Duration of treatment | | ● | ● | ● | | | | |
| 5 Contact rate | | ● | ● | ● | NYS scales | | | |
| 6 Improvement | | ● | ● | ● | primary scale | | | |
| 7 Remission | | ● | ● | ● | primary scale | | | |
| 8 Psychiatric consultation | | ● | ● | ● | primary scale | ● | | |
| 9 Screening rate | ● | | | | PHQ-2, PHQ-9, PHQ-A | | ● | ● |
| 10 Screening yield | | | | | PHQ-9, PHQ-A | | | |
| 11 BHCM FTE | | | | | | | | ● |
