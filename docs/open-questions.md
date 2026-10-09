# Open questions

Only what is still open. Each measure question raised after draft v0.1 (Q-01 – Q-09)
now has a call in [`our-calls.md`](reference/our-calls.md), and each call lists the
question it replaces. Every call still needs approval.

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

- A spot-check of the [LOINC codes](reference/instruments.md#loinc-codes) on loinc.org,
  which blocks automated access. They were checked against the HL7 terminology server
  and the NLM's LOINC index.
- The PCL-5 cutoff against the National Center for PTSD's own guidance, and the GAD-7
  severity bands against Spitzer et al. (2006).
- The qualifying-visit code list, including the telehealth codes.
- The CoCM billing codes used to infer enrollment when there's no enrollment record,
  including any codes FQHCs and rural health clinics bill for CoCM instead.

## The tooling

| ID | Question | Notes |
|---|---|---|
| Q-T1 | Which way in do we build first? | See the [tooling plan](tooling.md#what-to-build-first). |
| Q-T2 | Where does the calculator run? | In the browser on the site's machine (no patient data leaves the site), or as a script the site runs. |
| Q-T3 | How do sites pseudonymize `patient_id` consistently across sources? | The registry and the EHR must produce the same id for the same patient, or nothing joins. |

## About the guide

| Question | Notes |
|---|---|
| Whose calls are these? | "Our call" needs an "our": SPiER, HTD, a named working group, or unattributed. |
| Who approves a call? | Every call is marked **approval needed**. Someone has to be able to approve it: the same group, a clinical lead for the calls that need clinical sign-off, or NYS itself. |
