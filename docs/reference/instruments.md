# Instruments

The symptom scales NYS names, with each one's scoring, thresholds and LOINC codes, in one
place. The [scales and outcomes](../guide/concepts/scales-and-outcomes.md) page says how
the guide uses them.

## At a glance

| Instrument | Forms | Total score range | Elevated baseline at or above | Improved when (NYS) | Remission below | Firmness of our thresholds |
|---|---|---|---|---|---|---|
| PHQ-9 (and PHQ-A) | One | 0–27 | 10 | At most half the baseline, or below 10 | 5 | Our call, backed by HEDIS |
| GAD-7 | One | 0–21 | 10 | At most half the baseline, or below 10 | 5 | Our call |
| PCL-5 | One | 0–80 | 33 | At least 12 points below baseline | 33 | Needs clinical sign-off |
| SCARED | Child; caregiver | 0–82 | 25 | Either form at most half its baseline | 25 | Needs clinical sign-off |
| SMFQ | Child (SMFQ-C); parent (SMFQ-P) | 0–26 | 12 (child form) | Child form 8 points better, or parent form 6 | 8 (child form) | Needs clinical sign-off |
| PSC-17 | One | 0–34 | 15 | At most half the baseline | 15 | Needs clinical sign-off |
| NICHQ Vanderbilt | Parent; teacher | Subscale scores; no single total | Not set | Either form's score at most half its baseline | Fewer than 6 symptom items rated 2 or 3 | Needs clinical sign-off |

The improvement criteria are [NYS Appendix A](nys-source/nys-omh-cocm-metrics-2025.md#appendix-a-improvement-rate-specifications).
Elevated-baseline and remission thresholds are the guide's calls:
[elevated baseline](our-calls.md#elevated-baseline) and
[remission thresholds](our-calls.md#remission-thresholds).

## Where the thresholds come from

Checked against published sources on 9 October 2026. Each source is a scoring guide or
validation study, not a CoCM standard, so a clinician should still sign off on using it
as an elevated-baseline or remission threshold.

| Instrument | Threshold | Source |
|---|---|---|
| PHQ-9 | Elevated at 10 or more; remission below 5 | The HEDIS depression remission or response measure (DRR-E) starts from a PHQ-9 above 9 and defines remission as a most recent PHQ-9 below 5. See, for example, [Johns Hopkins Health Plans' summary of DRR-E](https://www.hopkinsmedicine.org/johns-hopkins-health-plans/providers-physicians/health-care-performance-measures/hedis/depression-remission-or-response-for-adolescents-and-adults) |
| GAD-7 | Elevated at 10 or more; remission below 5 | The GAD-7's own severity bands, with 5, 10 and 15 marking mild, moderate and severe (Spitzer et al., 2006). Not rechecked here |
| PCL-5 | 33 | Published guidance gives 31–33 as the range for probable PTSD (Bovin et al., 2016), per the [ISTSS PCL-5 resource page](https://istss.org/Clinical-Resources/Assessing-Trauma/PTSD-Checklist-DSM-5). The guide uses the top of that range. The National Center for PTSD's own page wasn't reachable to confirm |
| SCARED | 25 | The scale's scoring aid: a total of 25 or more may indicate an anxiety disorder, and above 30 is more specific (Birmaher et al., 1997). Example: [University of Florida copy of the parent form](https://com-psychiatry-dcf-a2.sites.medinfo.ufl.edu/files/2011/05/ScaredParent-final.pdf) |
| PSC-17 | 15 | The suggested total cutoff, from Gardner and Kelleher (1999). The subscale cutoffs are 5 internalizing, 7 attention and 7 externalizing. See the [University of Washington scoring sheet](https://depts.washington.edu/dbpeds/Screening%20Tools/PSC-17.pdf) |
| SMFQ | 12, child form | Supported for adolescents seeking help ([Thabrew et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6877137)). The developers recommend **no** single cutpoint ([Duke cut-point note](https://psychiatry.duke.edu/sites/default/files/2023-03/Cut%20Point%20Information%20for%20MFQ.pdf)). The remission threshold of 8 has no source yet |
| NICHQ Vanderbilt | — | No published remission threshold. The proposed rule borrows the DSM-5 symptom count: six or more symptoms in a domain |

## LOINC codes

Checked on 9 October 2026 against the HL7 terminology server (`tx.fhir.org`, LOINC
lookup and search) and the National Library of Medicine's
[Clinical Tables LOINC index](https://clinicaltables.nlm.nih.gov/). loinc.org itself
blocks automated access, so someone should spot-check these codes there.

| Instrument | Use this code for the total | Name in LOINC | Don't confuse with |
|---|---|---|---|
| PHQ-9 | `44261-6` | Patient Health Questionnaire 9 item (PHQ-9) total score [Reported] | — |
| PHQ-A | `89204-2` | Patient Health Questionnaire-9: Modified for Teens total score [Reported.PHQ.Teen] | `89206-7`, the panel |
| PHQ-2 | `55758-7` | Patient Health Questionnaire 2 item (PHQ-2) total score [Reported] | — |
| GAD-7 | `70274-6` | Generalized anxiety disorder 7 item (GAD-7) total score [Reported.PHQ] | `69737-5`, the GAD-7 **panel**, which isn't a score |
| PCL-5 | `101698-9` | PTSD PCL-5 score [PCL-5] | `101697-1`, the panel |
| NICHQ Vanderbilt, parent | No total. Subscale scores: `106402-1` inattention, `106403-9` hyperactivity or impulsivity, `106404-7` combined, `106408-8` performance | NICHQ Vanderbilt Assessment Scale - Parent Informant (`106345-2`, the panel) | — |
| NICHQ Vanderbilt, teacher | None found | — | — |
| SCARED (child or caregiver) | None found | — | LOINC's `[SCARED-R]` codes are for the SCARED-Revised, a different 66-item instrument |
| SMFQ (child or parent) | None found | — | LOINC's `[MFQ]` codes are for the **adult** Mood and Feelings Questionnaire |
| PSC-17 | None found | — | — |

**What this settles.** The GAD-7 total is `70274-6`. The archived draft was right, and
the prototype registry's `69737-5` is the panel code. That resolves archived review note
R-14 for the codes that exist.

**What it means for sites.** Four of the seven NYS instruments have no LOINC total
score code, and EHRs often store scale results under local codes anyway. So the
[data contract](data-contract.md) identifies instruments by name, and its `loinc` column
is optional. Where a site's results do carry LOINC codes, the codes above are the ones
to expect.
