# NYS CoCM Reporting Specification

**Status:** Draft v0.1 for review

**Source document:** NYS OMH, "The following metrics are reported for your Collaborative Care (CoCM) Caseload" (2025) — [`docs/source/nys-omh-cocm-metrics-2025.pdf`](../source/nys-omh-cocm-metrics-2025.pdf)

**Audience:** Reporting analysts, EHR report writers, registry administrators, and CoCM program leads

> **About this copy.** This is draft v0.1 as circulated, with decision owners removed.
> Known errors and gaps are listed in [`review-notes.md`](review-notes.md) and are
> deliberately **not** corrected here yet, so each correction stays traceable to a
> review note. Questions raised after v0.1 are in [`../open-questions.md`](../open-questions.md).

## Open Data Gaps

* **[MISSING]** LOINC codes for PCL-5, SMFQ, SCARED, PSC-17, NICHQ Vanderbilt
* **[MISSING]** Elevated baseline thresholds for pediatric scales (SMFQ, SCARED, PSC-17, Vanderbilt)
* **[MISSING]** NYS REDCap submission deadline and format constraints
* **[MISSING]** Whether NYS has an unpublished remission definition already in use by any site

## Section 1: Shared Definitions

### How to use this section

Every metric in Section 2 is written in terms of the definitions below. A site should implement each definition once as a reusable data element or query filter, then build the 11 metrics on top of them. If two metrics disagree about who counts as an enrolled patient, the fix is here, not in the metric.

Each definition has five parts:

* **Definition.** The rule, stated so that two analysts at different sites produce the same result.
* **Source data.** Where the element typically lives in an EHR or registry. Examples are illustrative, not required.
* **Used by.** Which metrics depend on this definition.
* **Common errors.** Mistakes observed in the field that produce wrong numbers.
* **Decision needed.** Items where the NYS source document is silent or ambiguous. Marked **[DECISION]** and collected in the log at the end of this section.

#### Required Data

1. Reporting Period
2. CoCM Enrollment
3. Enrollment Date
4. Discharge Date
5. Enrolled This Month
6. Days in Treatment
7. Medicaid Patient
8. Qualifying Visit
9. Universal Screening Population
10. Screening Scale vs. Monitoring Scale
11. Symptom-Monitoring Scale Result
12. Baseline Score
13. Primary Diagnosis and Primary Scale
14. Clinical Contact
15. Improvement Criteria
16. Remission Criteria
17. Psychiatric Consultation Event
18. BHCM FTE
19. Report Run Date

### D-01. Reporting Period

**Definition.** One calendar month, from 00:00 on the first day through 23:59:59 on the last day, in the site's local time zone. All "this month" language in the NYS metrics refers to the reporting period. Events are attributed to the period in which they occurred, not the period in which they were documented or billed.

**Source data.** Encounter date or contact date. Do not use claim date, posting date, or note signature date.

**Used by.** All metrics.

**Common errors.**

* Using service date for some metrics and documentation date for others, so patients appear in one month's denominator and the next month's numerator.
* Running reports before late documentation is complete. See D-17 for the recommended run date.

### D-02. CoCM Enrollment

**Definition.** A patient is enrolled in CoCM when all of the following are true:

1. A CoCM enrollment event has been recorded (registry enrollment, consent, or equivalent structured field), and
2. The patient has not been discharged (see D-04).

Verbal consent alone without a documented enrollment event does not count. A referral to CoCM does not count until enrollment is recorded.

**Source data.** Registry enrollment record. In EHR-only sites, a structured enrollment flag, episode of care, or program enrollment record. Billing of CoCM codes (99492, 99493, 99494, G2214) may be used as a fallback signal but is not the preferred source, because a patient can be enrolled and unbilled in a given month.

**Used by.** Metrics 1 through 8.

**Common errors.**

* Counting patients as enrolled from the referral date, which inflates enrollment and shortens apparent duration of treatment.
* Counting patients as enrolled only when a CoCM code was billed that month, which undercounts.

**[DECISION D-02a]** Confirm whether billing of CoCM codes is an acceptable fallback source for sites without a registry, or whether a structured enrollment record is required.

### D-03. Enrollment Date

**Definition.** The date of the initial CoCM assessment by the behavioral health care manager (BHCM). If the assessment spans more than one contact, use the date of the first contact in which a symptom-monitoring scale was administered as part of CoCM.

The NYS document uses "initial assessment" as the start point for Average Duration of Treatment (metric 4). This specification treats enrollment date and initial assessment date as the same date.

**Source data.** Registry enrollment date. Otherwise, date of the first BHCM encounter linked to the CoCM episode.

**Used by.** Metrics 3, 4, 6, 8.

**Common errors.**

* Using the referral date or the PCP's warm handoff date.
* Using the date the enrollment was keyed into the registry rather than the date the assessment happened.

### D-04. Discharge Date

**Definition.** The date the CoCM episode is closed in the registry or EHR for any reason, including graduation, loss to follow-up, patient withdrawal, transfer to specialty care, or death. A patient with no discharge date is considered enrolled.

**Source data.** Registry discharge date or episode end date.

**Used by.** Metrics 1, 2, 4, 5, 6, 7, 8 (as the boundary on "enrolled this month").

**Common errors.**

* Never discharging patients who stop engaging, which inflates enrollment and drives down Monthly Contact Rate.
* Backdating a discharge to the last contact date months after the fact, which changes prior months' reported numbers.

**[DECISION D-04a]** Confirm the inactivity rule. Recommended: a patient with no clinical contact for 90 consecutive days is administratively discharged as of the date of the last contact plus 90 days. NYS is silent on this.

### D-05. Enrolled This Month

**Definition.** A patient is "enrolled this month" if their enrollment period overlaps the reporting period by at least one day. Formally: Enrollment Date is on or before the last day of the month, AND (Discharge Date is null OR Discharge Date is on or after the first day of the month).

This is a "touched the month" rule, not a point-in-time snapshot. A patient enrolled on the 3rd and discharged on the 10th counts. A patient discharged on the 1st counts.

**Source data.** Derived from D-03 and D-04.

**Used by.** Metrics 1, 2, 5, 6, 7, 8.

**Common errors.**

* Counting enrollment as of the last day of the month only, which drops everyone discharged mid-month and understates the denominator for metrics 5 and 7.
* Counting patients enrolled at any point in the year.

**[DECISION D-05a]** Confirm the overlap rule vs. a month-end snapshot. The overlap rule is recommended because metrics 5 and 7 measure activity during the month, and a patient who received treatment and then graduated on the 20th should count in both numerator and denominator.

### D-06. Days in Treatment

**Definition.** The number of calendar days from Enrollment Date (D-03) to the last day of the reporting period, or to Discharge Date (D-04) if discharged during the period, inclusive of the enrollment date.

The NYS document uses "70 days or greater" in metrics 6 and 8 and "at least 10 weeks" in Appendix A. This specification treats them as equivalent: 70 days.

**Source data.** Derived from D-01, D-03, D-04.

**Used by.** Metrics 4, 6, 8.

**Common errors.**

* Measuring from referral date.
* Measuring to the report run date rather than the end of the reporting period.

### D-07. Medicaid Patient

**Definition.** A patient whose primary coverage on the first day of the reporting period is New York State Medicaid, either fee-for-service or a Medicaid managed care plan. Patients dually eligible for Medicare and Medicaid count as Medicaid patients. Patients whose coverage changes mid-month are classified by their coverage on the first day of the month.

**Source data.** Coverage or insurance record active on the first of the month. Payer class or financial class field mapped to Medicaid. Registry payer field if the registry captures it.

**Used by.** Metrics 2 through 8.

**Common errors.**

* Using payer as of the report run date, which reclassifies patients retroactively.
* Excluding Medicaid managed care because it is listed under the plan name (Fidelis, Healthfirst, etc.) rather than "Medicaid."
* Excluding dual eligibles.
* Applying the Medicaid filter to metrics 1, 9, 10, or 11, which are all-payer metrics.

**[DECISION D-07a]** Confirm the first-of-month attribution rule and the treatment of dual eligibles. Confirm whether Child Health Plus or Essential Plan should be treated as Medicaid for this reporting.

### D-08. Qualifying Visit

**Definition.** An in-person or telehealth encounter with a medical (non-behavioral-health) provider at the practice, billed or billable with an evaluation and management (E&M) or preventive medicine code, during the reporting period.

Included code families:

* Office or outpatient E&M: 99202 through 99215
* Preventive medicine, new and established: 99381 through 99397
* Annual wellness visit: G0438, G0439
* Telehealth equivalents of the above when billed with modifier 95 or GT, or with codes 98000 through 98015

Excluded from qualifying visits:

* Encounters with the BHCM, psychiatric consultant, or any behavioral health provider
* Nurse-only visits, injection visits, lab draws, vaccine-only visits
* Visits with diabetes educators, nutritionists, care coordinators, or community health workers
* Telephone check-ins without a billable E&M service
* Portal messages

**Source data.** Encounter record with provider type and CPT code. In EHRs, this is usually the encounter or visit table joined to the charge or procedure table.

**Used by.** Metric 9 (denominator).

**Common errors.**

* Counting every encounter of any type, which inflates the screening denominator with lab visits and nurse visits.
* Counting BHCM contacts as visits, which both inflates the denominator and, because the BHCM administers PHQs as part of treatment, inflates the numerator. This is the single most common error observed.
* Counting visits to behavioral health clinicians who do not bill E&M.

**[DECISION D-08a]** Confirm the code list. Confirm whether the practice should include visits from any medical provider or only PCPs (for example, whether an OB or pediatric visit counts at a multi-specialty site).

### D-09. Universal Screening Population

**Definition.** Patients aged **[DECISION]** or older on the date of a Qualifying Visit (D-08). The NYS document says "patients that meet practice criteria for universal depression screen (Refer to practice workflow)," which leaves the age floor to each site. For the purpose of consistent reporting, a single age floor must be set.

**Source data.** Patient date of birth compared to visit date.

**Used by.** Metric 9 (denominator).

**Common errors.**

* Including patients aged 0 to 11, which inflates the denominator with patients who are not screened by any standard PHQ workflow.
* Using age at report run date rather than age at visit.

**[DECISION D-09a]** Set the age floor. Options: 12 (aligns with USPSTF adolescent depression screening and PHQ-A validation) or 18 (adult only). Both have been discussed. Recommended: 12, with a note that pediatric-only practices may report the same floor.

**[DECISION D-09b]** Confirm whether any exclusions apply (for example, patients already enrolled in CoCM, patients with a documented bipolar or psychotic disorder diagnosis, or patients who declined screening). NYS does not list any. Recommended: no exclusions in the denominator; declined screenings do not count in the numerator.

### D-10. Screening Scale vs. Monitoring Scale

**Definition.** The same instrument (PHQ-2, PHQ-9) is used for two different purposes, and reports must distinguish them by context.

* A **screening scale** is a PHQ-2 or PHQ-9 administered during or in connection with a Qualifying Visit (D-08), by or on behalf of the medical provider, to a patient not currently enrolled in CoCM or as part of the practice's annual universal screening workflow.
* A **monitoring scale** is any symptom scale administered by the BHCM, psychiatric consultant, or behavioral health team to a patient enrolled in CoCM as part of treatment.

Monitoring scales never count toward metric 9 or metric 10. Screening scales never count toward metrics 5, 6, 7, or 8.

**Source data.** The distinguishing attribute is the encounter or ordering context, not the instrument. Options in priority order:

1. Encounter type or department (medical vs. behavioral health)
2. Administering provider type
3. Registry vs. EHR as the source system (registry entries are monitoring by definition)

**Used by.** Metrics 5 through 10.

**Common errors.**

* Pulling all PHQ-9 results from a flowsheet or questionnaire table regardless of who administered them, which pushes every BHCM monitoring PHQ into the screening numerator.

### D-11. Symptom-Monitoring Scale Result

**Definition.** A completed, scored administration of one of the NYS-approved instruments, recorded as a structured value with a date. Partially completed instruments without a total score do not count.

Approved instruments per NYS: PHQ-9, GAD-7, PCL-5, SMFQ (child and parent), SCARED (child and parent), PSC-17, NICHQ Vanderbilt (parent and teacher).

**Source data.** Registry scale table. In EHRs, a questionnaire, flowsheet, or observation table with a structured total score. Where sites use LOINC, common total-score codes include PHQ-9 total 44261-6, GAD-7 total 70274-6, PHQ-2 total 55758-7. **[MISSING]** LOINC codes for PCL-5, SMFQ, SCARED, PSC-17, and Vanderbilt to be verified and listed in Appendix C.

**Used by.** Metrics 5, 6, 7, 8.

**Common errors.**

* Counting a scale as completed when it was ordered or offered but not scored.
* Counting a free-text note stating "PHQ-9 administered" without a score.

### D-12. Baseline Score

**Definition.** The first Symptom-Monitoring Scale Result (D-11) on the patient's primary scale (D-13) recorded on or within 14 days after the Enrollment Date (D-03). If more than one result falls in that window, use the earliest. If no result falls in that window, the baseline is the first result recorded after enrollment on the primary scale.

An **elevated baseline** is one that meets the per-scale threshold in Appendix B (for example, PHQ-9 of 10 or greater). Appendix A of the NYS document states that patients must have an elevated baseline to be included in the Improvement Rate.

**Source data.** Registry baseline field if present. Otherwise derived from D-11 and D-03.

**Used by.** Metrics 6, 8.

**Common errors.**

* Using a screening PHQ from weeks before enrollment as the baseline.
* Resetting the baseline when a patient is re-enrolled without closing and reopening the episode.

**[DECISION D-12a]** Confirm the 14-day window and the fallback rule.

**[DECISION D-12b]** Confirm elevated baseline thresholds for each scale. NYS states the requirement but does not define the thresholds. Recommended thresholds are proposed in Appendix B for review.

### D-13. Primary Diagnosis and Primary Scale

**Definition.** The primary diagnosis is the behavioral health condition the CoCM episode is treating, as recorded in the registry or the CoCM problem list at enrollment. The primary scale is the single symptom-monitoring instrument that corresponds to that diagnosis. NYS Appendix A states that patients count toward improvement "when they meet criteria for the scale used to treat their primary diagnosis."

Default mapping:

* Depressive disorders: PHQ-9
* Anxiety disorders: GAD-7 (adults), SCARED (children and adolescents)
* PTSD: PCL-5
* Adolescent depression: SMFQ or PHQ-9 (site chooses one at enrollment)
* ADHD: NICHQ Vanderbilt
* General pediatric behavioral concern: PSC-17

**Source data.** Registry primary diagnosis or target condition field. Otherwise the ICD-10 diagnosis linked to the CoCM episode.

**Used by.** Metrics 6, 7, 8.

**Common errors.**

* Counting a patient as improved if any scale improved, rather than the primary scale.
* Changing the primary scale mid-episode.

**[DECISION D-13a]** Confirm the default mapping and whether a site may designate a different primary scale at enrollment.

### D-14. Clinical Contact

**Definition.** A documented interaction between the BHCM (or another CoCM team member delivering treatment) and the patient or caregiver, in which treatment is delivered. Modalities include in-person, video, and telephone. The NYS note states that a clinical contact is one "in which symptom monitoring may occur and treatment is delivered with corroborating documentation in the patient chart."

* Included: BHCM follow-up sessions, behavioral activation or brief therapy sessions, medication adherence check-ins with clinical content, caregiver sessions for pediatric patients.
* Excluded: appointment scheduling calls, reminder calls, no-shows, unanswered outreach attempts, portal messages without clinical content, psychiatric case review (which is a team contact, not a patient contact, and is tracked separately under D-16).

**Source data.** Registry contact log. In EHRs, BHCM encounters or telephone encounters with a signed note.

**Used by.** Metric 5.

**Common errors.**

* Counting outreach attempts as contacts.
* Counting the psychiatric consultant's caseload review as a patient contact.

**[DECISION D-14a]** Confirm whether a minimum contact duration applies. NYS does not specify one. Recommended: none, documentation of treatment content is the test.

### D-15. Improvement Criteria

**Definition.** Per NYS Appendix A, reproduced here for reference and expanded in Appendix B:

| Scale | Improvement criteria (compared to Baseline Score, D-12) |
| :---- | :---- |
| PHQ-9 | 50% or greater reduction OR current score below 10 |
| GAD-7 | 50% or greater reduction OR current score below 10 |
| PCL-5 | Reduction of 12 or more points |
| NICHQ Vanderbilt | 50% or greater reduction on parent OR teacher form |
| SCARED | 50% or greater reduction on caregiver and/or youth form |
| SMFQ | Child form reduced 8 or more points OR parent form reduced 6 or more points |
| PSC-17 | 50% or greater reduction |

"Current score" means the most recent Symptom-Monitoring Scale Result (D-11) on the primary scale recorded on or before the last day of the reporting period.

**Used by.** Metrics 6, 8.

**Common errors.**

* Comparing to the previous month's score rather than baseline.
* Using any scale rather than the primary scale.

**[DECISION D-15a]** Confirm whether a patient with no scale result in the current month uses their most recent prior result, or is treated as not improved. Recommended: most recent prior result, with no lookback limit within the episode.

### D-16. Remission Criteria

**Definition.** NYS metric 7 requires "remission criteria" but the source document does not define them anywhere. Proposed definition, pending confirmation:

| Scale | Remission criteria |
| :---- | :---- |
| PHQ-9 | Current score below 5 |
| GAD-7 | Current score below 5 |
| PCL-5 | Current score below 33 |
| SMFQ | Child form below 8 |
| SCARED | Total below 25 |
| PSC-17 | Total below 15 |
| NICHQ Vanderbilt | **[MISSING]** No standard remission threshold. Proposed: fewer than 6 symptom items rated 2 or 3. |

Remission is assessed on the primary scale (D-13) using the most recent result on or before the last day of the reporting period.

**Used by.** Metric 7.

**[DECISION D-16a]** Confirm remission thresholds. PHQ-9 and GAD-7 below 5 align with HEDIS DRR and the AIMS Center's standard. The remaining thresholds are proposed from instrument literature and need clinical sign-off.

### D-17. Psychiatric Consultation Event

**Definition.** A documented case review by the psychiatric consultant in which the patient's case was discussed and treatment recommendations were communicated to the PCP or BHCM. Documentation must include the review date and a recommendation. A consultant note that lists the patient as "reviewed, no change" counts if a recommendation to continue current treatment is stated.

The 60-day lookback in metric 8 is measured backward from the last day of the reporting period. A review on any date within that 60-day window counts.

**Source data.** Registry consultation log. In EHRs, a psychiatric consultant note or a structured case review field linked to the patient.

**Used by.** Metric 8.

**Common errors.**

* Counting a consultant's presence at a caseload review meeting as a review of every patient on the caseload.
* Measuring the 60 days from the report run date.

### D-18. BHCM FTE

**Definition.** The sum of full-time-equivalent effort devoted to CoCM care management during the reporting period, where 1.0 FTE equals the site's standard full-time schedule. A BHCM who spends 60% of a full-time schedule on CoCM and 40% on other duties contributes 0.6. Psychiatric consultant time and PCP time are not included.

**Source data.** Staffing or HR records. Site attestation is acceptable.

**Used by.** Metrics 1 (optimal caseload reference), 11.

**[DECISION D-18a]** Confirm whether supervisors, trainees, or care coordinators supporting the BHCM count toward FTE.

### D-19. Report Run Date

**Definition.** Reports for a reporting period should be run no earlier than 15 days after the end of the month to allow documentation and coding to close. Once submitted to NYS, a month's numbers should not be restated except to correct an error.

**Used by.** All metrics (operational).

**[DECISION D-19a]** Confirm the lag with NYS submission deadlines.

## Decision Log

Items where the NYS source document is silent or ambiguous. Each needs a decision before Section 2 is final. Further questions raised after v0.1 are in [`../open-questions.md`](../open-questions.md).

| ID | Topic | Recommended |
| :---- | :---- | :---- |
| D-02a | Billing codes as fallback enrollment source | Allow with disclosure |
| D-04a | Inactivity discharge rule | 90 days no contact |
| D-05a | "Enrolled this month" overlap vs. snapshot | Overlap |
| D-07a | Medicaid attribution and dual eligibles, CHP, Essential Plan | First of month, include duals, exclude CHP and EP |
| D-08a | Qualifying visit code list and provider scope | E&M and preventive, all medical providers |
| D-09a | Screening age floor | 12 |
| D-09b | Screening denominator exclusions | None |
| D-12a | Baseline window | 14 days after enrollment |
| D-12b | Elevated baseline thresholds by scale | Appendix B proposal |
| D-13a | Primary scale mapping | Default table above |
| D-14a | Minimum contact duration | None |
| D-15a | Missing current-month score | Carry forward most recent |
| D-16a | Remission thresholds by scale | Table above |
| D-18a | Who counts toward BHCM FTE | BHCMs only |
| D-19a | Report run lag | 15 days |
