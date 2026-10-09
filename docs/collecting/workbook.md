# The workbook route

For sites whose CoCM registry is a spreadsheet, or that have no report writer. The site
fills in the reporting workbook each month, from its registry spreadsheet and two or
three standard reports, then adds the workbook to the
[calculator page](https://spier-project.github.io/nys-omh-cocm-caseload-reporting/).
The page calculates the eleven metrics in the browser; the workbook is never uploaded.

## Download

- [Blank workbook](https://spier-project.github.io/nys-omh-cocm-caseload-reporting/cocm-workbook.xlsx)
- [Example workbook](https://spier-project.github.io/nys-omh-cocm-caseload-reporting/cocm-workbook-example.xlsx),
  filled with the guide's [example caseload](../guide/example-caseload.md). Add it to the
  calculator page to see how the numbers come out.

They open in Excel, Google Sheets, Numbers and LibreOffice.

## What's in it

- **Instructions:** how to fill it in.
- **One tab per table** of the [data contract](../reference/data-contract.md), with the
  column names in the first row:
  - a dropdown on every column with fixed values;
  - date and number checks;
  - a note on each column, shown when you click into it.
- **Columns:** every column of every tab, with what it holds and the values it allows.

The workbook is built from the data contract by `scripts/build_workbook.py`, so its
columns always match what the calculator reads.

## Filling it in

- **Use the same patient id on every tab:** a registry number or another id the site
  assigns, never a name. The workbook and the results stay at the site.
- **One row per fact,** not one row per patient:
  - one `cocm_episode` row per enrollment, so a returning patient gets a new row;
  - one `contact` row per contact or outreach attempt;
  - one `scale_result` row per completed, scored scale;
  - one `psych_review` row per patient discussed.

  Tick columns ("contacted this month") don't carry enough to calculate the metrics; the
  dates and the kind of contact matter.
- **Add each month's rows; don't start over.** The calculator looks back as far as it
  needs: to each episode's enrollment for contacts and scales, and
  <!--rule:extraction.phq_history_months-->13<!--/rule--> months for practice-wide PHQs.
  Keep one workbook going, and add the new month's facts to it.
- **Fill in one `site_month` row** for the month being reported: BHCM FTE, the screening
  age floor, and how contacts were judged to be treatment.

## Where each tab's facts come from

| Tab | From |
|---|---|
| `patient`, `cocm_episode`, `contact`, `scale_result`, `psych_review` | The registry spreadsheet |
| `coverage` | A coverage report from the practice-management system: patient, payer, plan, effective dates. Map each plan to a payer category using the site's [payer mapping](../guide/concepts/medicaid.md#what-the-program-should-do) |
| `practice_visit` | A visits report: patient, visit date, provider type, billing codes. This is the hardest report, and the one most worth asking a vendor or billing service to set up once |
| `scale_result` (screening) | A PHQ-2 and PHQ-9 report for the whole practice: patient, date, instrument, score |
| `site_month` | The program lead |

## What a registry spreadsheet often lacks

| Needed | Often missing? |
|---|---|
| Enrollment date: the date of the initial assessment | Sometimes the referral date instead |
| Discharge date and reason | Often blank for patients who drifted away |
| Primary diagnosis and **primary scale** | Primary scale usually missing |
| Each scale result with its own date | Dates often missing; a score in the "March" column isn't enough near month end |
| Each contact, with whether treatment was delivered | Often a single "contacted this month" tick, with no way to tell a session from a reminder call |
| Outreach attempts | Often not recorded |
| Each psychiatric case review, with whether a recommendation was documented | Often a single "reviewed" tick |

## Checks before submitting

- Does the number of enrolled patients match the caseload the BHCMs think they have?
- Does every patient enrolled <!--rule:seventy-days.days-->70<!--/rule--> days or more have a primary scale and a baseline?
- Is anyone enrolled with no clinical contact in the last <!--rule:inactivity-discharge.days-->90<!--/rule--> days? They should be
  re-engaged or discharged.
- Does every Medicaid managed care plan in the coverage report appear in the payer
  mapping?
- Read the calculator's list of who fell out of each numerator. The patients on it
  should be the ones the team would expect.
