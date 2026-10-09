# Review notes on draft v0.1

Each note compares [`reporting-spec-draft.md`](reporting-spec-draft.md) against the
NYS source document ([`../source/nys-omh-cocm-metrics-2025.pdf`](../source/nys-omh-cocm-metrics-2025.pdf)).
None is applied to the draft yet. When one is, the commit should cite its id.

Notes that need a policy answer, not just an edit, are also carried as questions in
[`../open-questions.md`](../open-questions.md).

## Where the draft changes the source

**R-01. D-08 narrows the metric 9 denominator.** NYS counts patients "seen in the
practice for any reason this month." D-08 counts only office, preventive and wellness
visits with a medical provider. That may be the better rule, but it changes the measure,
so it belongs in the decision log as a choice, not in the definition as a fact. → Q-01

**R-02. Metric 9 counts patients; D-08 defines visits.** The draft never says to count
each patient once per month.

**R-03. Remission is "during this month" in the source.** Metric 7 counts patients who
"have achieved remission criteria during this month." D-16 uses the most recent result
on or before month end with no lookback limit, so a score from months ago keeps a
patient in remission. Those are different measures. → Q-02

**R-04. Remission has no elevated-baseline requirement.** As written, a patient who
enrolls with a PHQ-9 of 4 is in remission on the day they enroll. Improvement has the
guard (Appendix A); remission needs one too, or an explicit decision that it doesn't. → Q-03

## Where the draft contradicts itself

**R-05. Enrolled CoCM patients are penalized on metric 9.** D-09b keeps enrolled patients
in the screening denominator, and D-10 says their monitoring PHQ-9s never count toward
screening. An enrolled patient with a PHQ-9 last week therefore counts as unscreened
unless someone screens them again. The source numerator ("have been screened in the last
12 months") arguably accepts any PHQ. → Q-04

**R-06. Metric 8 has no ruling on elevated baseline.** Its denominator is the patients
who did not meet improvement criteria. Whether a patient who never had an elevated
baseline is in it is not decided. → Q-05

**R-07. The 70-day count is off by one.** D-06 counts "inclusive of the enrollment date,"
so a patient reaches day 70 after 69 elapsed days.

**R-08. Metric 4 has no days-to-weeks rule.** The source asks for an average in weeks;
the draft does not say whether to divide days by 7 before or after averaging, or how to
round.

## Terms the draft does not define

**R-09. "Diagnosed" in metric 3.** The source counts patients "diagnosed and enrolled in
CoCM this month." The draft treats it as enrolled only. → Q-06

**R-10. "Initial PHQ-9" in metric 10.** First ever, first in 12 months, or first in the
month? The answer sets the yield denominator. → Q-07

## Editorial

**R-11. Cross-references.** D-01 points to D-17 for the run date; it is D-19. D-14 points
to D-16 for psychiatric review; it is D-17.

**R-12. Appendices B and C are referenced but do not exist.** D-12 and D-15 point to
Appendix B for thresholds; D-11 points to Appendix C for codes.

**R-13. An unsourced field claim.** D-08 calls counting BHCM contacts as visits "the
single most common error observed." Either cite where that was observed or soften it;
a state reviewer will ask.

**R-14. Codes need a terminology check before publication.** The three LOINC codes in
D-11 were confirmed from memory in review, which is the mistake this note warns
against. A prototype CoCM registry's documentation gives the GAD-7 total as `69737-5`,
where D-11 gives `70274-6`; at least one is wrong or a variant. Every code, listed and
missing, should be looked up against LOINC itself, not recalled.
