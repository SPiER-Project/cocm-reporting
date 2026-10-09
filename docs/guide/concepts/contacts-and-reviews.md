# Contacts and reviews

Two kinds of CoCM activity NYS counts:
- **Clinical contacts:** the care team treating the patient.
- **Psychiatric case reviews:** the consultant reviewing the patient's case with the team.

They are easy to confuse. Either one gets inflated when an attempt or a meeting is
counted as the real thing.

**Used by:** metric 5 (contacts) and metric 8 (reviews).

## What NYS says

- Metric 5 counts patients "receiving active treatment": "at least one clinical contact
  and symptom-monitoring scale completed this month."
- A clinical contact is "a contact in which symptom monitoring may occur and treatment is
  delivered with corroborating documentation in the patient chart. This includes virtual
  engagement if treatment is delivered."
- Metric 8 counts patients "whose case was reviewed by the Psychiatric Consultant with
  treatment recommendations provided to the PCP or BHCM in the past 60 days."

([Source](../../reference/nys-source/nys-omh-cocm-metrics-2025.md#5-monthly-contact-rate))

## The rule

### Clinical contact

A clinical contact is a **documented, live interaction** in which the BHCM, or another
CoCM clinician, **delivers treatment** to the patient. For a child, a contact with the
caregiver counts too. It can be in person, by video or by phone. There is no minimum
length; what makes it a contact is that the note documents treatment. *Our call:
[clinical contact](../../reference/our-calls.md#clinical-contact).*

| Counts | Doesn't count |
|---|---|
| BHCM follow-up sessions | Scheduling and reminder calls |
| Behavioral activation, problem-solving or other brief therapy sessions | No-shows |
| Medication adherence check-ins that address treatment | Unanswered calls, voicemails, outreach letters |
| Caregiver sessions for a pediatric patient | Portal messages, texts and email, **even with clinical content** |
| Video and phone sessions where treatment is delivered | The psychiatric consultant's case review |

Excluding all messages is stricter than the archived draft. A message can contain
clinical content, but it's hard to show in a chart that treatment was delivered, and a
reviewer would have to read every message to decide.

### Active treatment (metric 5)

A patient is in active treatment this month when they have **both** of these:

- **A clinical contact** this month.
- **A scored scale** this month. It can be any of the seven NYS scales, not only the
  primary scale, and it must be dated on or after the enrollment date.

The two don't have to happen on the same day. A PHQ-9 sent through the portal the day
before a phone session counts. *Our call:
[active treatment](../../reference/our-calls.md#active-treatment).*

### Psychiatric case review (metric 8)

A case review counts when the psychiatric consultant **reviewed this patient** and a
**recommendation to the PCP or BHCM is documented**. "Continue current treatment" is a
recommendation. *Our call:
[psychiatric case review](../../reference/our-calls.md#psychiatric-case-review).*

- **It's per patient.** The consultant attending the weekly caseload meeting is not a
  review of everyone on the caseload. Only the patients discussed, with a recommendation
  recorded, count.
- **The window is the <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days ending on the last day of the month**, counting both ends.
  For March 2025 that's 31 January to 31 March. Count back from month end, not from the
  date the report is run.
- A case review is not a clinical contact. A visit in which the consultant sees the
  patient directly is a contact if treatment is delivered, but it isn't a case review
  unless a recommendation to the PCP or BHCM is documented.

## Worked example

Reporting month: March 2025. All patients enrolled before March, all Medicaid.

| Patient | In March | Active treatment? |
|---|---|---|
| A | Phone session 4 Mar; PHQ-9 of 12 on 4 Mar | **Yes** |
| B | Video session 11 Mar; PHQ-9 completed in the portal 10 Mar | **Yes**: the two don't have to be on the same day |
| C | In-person session 18 Mar; no scale given | No: no scale |
| D | PHQ-9 completed in the portal 5 Mar; three unanswered calls | No: no clinical contact |
| E | Portal exchange about coping skills 20 Mar; GAD-7 the same day | No: a message isn't a clinical contact |
| F | Phone session 25 Mar; GAD-7 on 25 Mar, but primary scale is PHQ-9 | **Yes**: any NYS scale counts for metric 5 |

Metric 5 for these six: 3 of 6, or **50.0%**.

## What the program should do

- **Give a scale at every treatment contact**, or at least once a month. Patient C is
  the most common way to miss metric 5.
- **Document what treatment was delivered** in the contact note, not just that the
  patient was reached.
- **Log outreach attempts, but separately from contacts.** They show a caseload that
  isn't being reached, and they're the evidence for the
  [inactivity discharge](enrollment-and-discharge.md#discharge).
- **Record case reviews patient by patient**, with the recommendation, on the day of the
  review. A meeting note listing twenty names with no recommendations doesn't count for
  any of them.
- **Review every patient who isn't improving at least every <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days.** Metric 8's
  denominator is exactly those patients.

## Where the data lives

| Fact | Registry | EHR without a registry |
|---|---|---|
| Clinical contacts | The contact log, if it records the contact's purpose or outcome | BHCM encounters and telephone encounters with a signed note |
| Outreach attempts | Usually only in the registry's contact log | Telephone encounters with no note, or not recorded at all |
| Who made the contact | Contact author, if recorded | Encounter provider |
| Case reviews | A consultation or case-review log, one row per patient | Consultant notes; rarely a structured field. Often the hardest fact to extract |

- **Registries often record only whether the patient was reached**, not whether treatment
  was delivered. A scheduling call and a session then look the same. The
  [prototype registry mapping](../../collecting/registries/prototype-cocm-registry.md#t4-contact--patientcontact)
  shows the gap and a stricter rule that uses same-day progress notes.
- **Don't build case reviews from attendance or time logs.** A record that the consultant
  spent an hour at the caseload meeting says nothing about which patients were reviewed.
  Nor does one note per meeting.

## Common mistakes

| Mistake | Effect |
|---|---|
| Counting outreach attempts as contacts | Contact rate overstated |
| Counting a contact with no scale, or a scale with no contact | Contact rate overstated |
| Counting the consultant's caseload meeting as a review of every patient | Metric 8 overstated |
| Measuring the <!--rule:psychiatric-case-review.window_days-->60<!--/rule--> days from the run date | The window shifts; reviews early in the window drop out |
| Counting the case review as a patient contact | Contact rate overstated for patients discussed but not seen |

## For automation

- [`contact`](../../reference/data-contract.md#t4-contact--one-row-per-bhcm-or-team-interaction-with-the-patient)
  holds every interaction, including attempts and messages. Only `contact_kind =
  treatment` counts as a clinical contact.
- [`psych_review`](../../reference/data-contract.md#t6-psych_review--one-row-per-patient-discussed)
  is one row per patient discussed, never one per meeting. Only
  `recommendation_documented = true` counts.
- Active treatment is derived by the calculator from `contact` and `scale_result`.
