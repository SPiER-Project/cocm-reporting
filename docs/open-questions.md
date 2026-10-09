# Open questions

Questions raised after draft v0.1. The draft's own decision log (D-02a … D-19a) is in
[`spec/reporting-spec-draft.md`](spec/reporting-spec-draft.md#decision-log) and is not
repeated here.

Questions about the measures need an answer from the program and NYS. Questions about
the tooling (Q-T*) are ours to decide.

## The measures

| ID | Question | Raised by | Notes |
|---|---|---|---|
| Q-01 | Is the metric 9 denominator every patient seen "for any reason", or only qualifying medical visits? | R-01 | The [data contract](data-contract.md) extracts every visit with its provider type and codes, so either answer is a calculator setting. |
| Q-02 | Does remission (metric 7) need a qualifying score **in the month**, or does the most recent score carry forward? | R-03 | The source says "during this month". |
| Q-03 | Does remission require an elevated baseline? | R-04 | Without it, a patient can be in remission on the day they enroll. |
| Q-04 | Can a CoCM patient's monitoring PHQ count as "screened" for metric 9? | R-05 | If not, enrolled patients drag the screening rate down. |
| Q-05 | Is the metric 8 denominator limited to patients with an elevated baseline? | R-06 | It inherits "did not meet improvement criteria" from metric 6. |
| Q-06 | What does "diagnosed" add to metric 3, and from what date? | R-09 | Adds an optional `diagnosis_date` column if it matters. |
| Q-07 | What is an "initial" PHQ-9 in metric 10? | R-10 | "First in 12 months" is computable from the extract; "first ever" is not. |
| Q-08 | The Vanderbilt has no single total. Which score do improvement and remission use? | Data contract | Improvement (50%) and the proposed remission rule (fewer than 6 symptoms) need different numbers. |
| Q-09 | For SCARED and SMFQ, how are the child and caregiver forms paired? | Data contract | Two baselines and two current scores, possibly on different dates. Does either form meeting criteria count, and must the forms share a date? |

## The tooling

| ID | Question | Notes |
|---|---|---|
| Q-T1 | Which way in do we build first? | See [filling-the-tables.md](filling-the-tables.md#what-to-build-first). |
| Q-T2 | Where does the calculator run? | In the browser on the site's machine (no patient data leaves the site), or as a script the site runs. |
| Q-T3 | How do sites pseudonymize `patient_id` consistently across sources? | The registry and the EHR must produce the same id for the same patient, or nothing joins. |
| Q-T4 | Does NYS want patient-level data, or only the eleven numbers? | Assumed: only the numbers, in the REDCap form's shape. The patient-level detail stays at the site. |
| Q-T5 | What are the REDCap form's fields and deadline? | Also listed as a gap in the draft. The calculator's output should match the form exactly. |
