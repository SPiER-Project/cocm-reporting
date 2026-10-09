# Open questions

Only what is still open. Each measure question raised after draft v0.1 (Q-01 – Q-09)
now has a call in [`our-calls.md`](reference/our-calls.md), and each call lists the
question it replaces. Those calls are still **Proposed** until the project adopts them.

## For NYS

| Question | Notes |
|---|---|
| What are the REDCap form's fields and the submission deadline? | The deadline may override the [15-day run lag](reference/our-calls.md#when-to-run-the-report). The calculator's output should match the form exactly. (Q-T5) |
| Does NYS want patient-level data, or only the eleven numbers? | Assumed: only the numbers. The patient-level detail stays at the site. (Q-T4) |
| Does NYS already use a remission definition at any site? | If so, it replaces our [remission thresholds](reference/our-calls.md#remission-thresholds). |

## For a clinician

Calls marked **Needs clinical sign-off** in [`our-calls.md`](reference/our-calls.md):

- Elevated-baseline thresholds for PCL-5, SCARED, PSC-17, SMFQ and NICHQ Vanderbilt.
- Remission thresholds for the same five scales, including the Vanderbilt symptom-count rule.

## To verify against a source

Things stated from memory, which is the mistake the archived review note R-14 warns
about:

- LOINC codes for every instrument, starting with the GAD-7 total (`70274-6` in the
  draft, `69737-5` in the prototype registry).
- The candidate elevated-baseline cutoffs for PCL-5, SCARED and PSC-17.
- That HEDIS and the AIMS Center use PHQ-9 and GAD-7 below 5 for remission.
- The qualifying-visit code list, including the telehealth codes.

## The tooling

| ID | Question | Notes |
|---|---|---|
| Q-T1 | Which way in do we build first? | See [filling-the-tables.md](filling-the-tables.md#what-to-build-first). |
| Q-T2 | Where does the calculator run? | In the browser on the site's machine (no patient data leaves the site), or as a script the site runs. |
| Q-T3 | How do sites pseudonymize `patient_id` consistently across sources? | The registry and the EHR must produce the same id for the same patient, or nothing joins. |

## About the guide

| Question | Notes |
|---|---|
| Whose calls are these? | "Our call" needs an "our": SPiER, HTD, a named working group, or unattributed. |
