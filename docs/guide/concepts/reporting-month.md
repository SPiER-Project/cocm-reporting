# Reporting month

Every NYS metric is about "this month". This page says which month an event belongs to,
when to run the report, and when a submitted month can change.

**Used by:** all eleven metrics.

## What NYS says

Every metric says "this month" or "during the reporting period", and none defines it.
Metric 9 also looks back 12 months, and metric 8 looks back 60 days.

## The rule

**The month is the calendar month in the site's local time zone.** It runs from 00:00 on
the 1st to the end of the last day. *Our call:
[reporting month](../../reference/our-calls.md#reporting-month).*

**An event belongs to the month it happened in.** Use the date of service, contact,
administration or review. Don't use the date the note was signed, the claim was posted,
or the record was keyed in. *Our call.*

**Convert timestamps to local time before taking the date.** Many systems store
timestamps in UTC. In New York, a PHQ-9 completed at 9 p.m. on 31 March is stored as
1 April in UTC, which moves it into the wrong month. *Our call.*

**Run the report no earlier than the 15th of the following month.** That gives late
notes, scales and charges two weeks to land. *Our call:
[when to run the report](../../reference/our-calls.md#when-to-run-the-report).*
If NYS's deadline turns out to be earlier, the deadline wins.

**Don't restate a submitted month except to correct an error.** Late documentation that
arrives after the run belongs to the month it happened in, but it doesn't reopen a month
already submitted. A correction is a mistake in the extract or the logic, not a late note.
*Our call.*

## What the program should do

- Set a standing date for the monthly run, on or after the 15th.
- Ask clinicians to document contacts and scales within the month, or within two weeks of
  month end at the latest.
- Keep a short log of any month restated, and why.

## Where the data lives

Every source system has more than one date on a record. Use the one that says when the
event happened:

| Event | Use | Not |
|---|---|---|
| Contact or visit | Date of service | Note signature date, claim date |
| Scale result | Date administered | Date entered, date of the note it's attached to |
| Enrollment | Date of the initial assessment | Date the registry record was created |
| Discharge | Discharge date as recorded | Date the record was last updated, audit-log date |
| Psychiatric review | Date of the review | Date the consultant's note was signed |

Registries built on databases often store the event date as a UTC timestamp. The
[prototype registry mapping](../../collecting/registries/prototype-cocm-registry.md) shows one
example.

## Common mistakes

| Mistake | Effect |
|---|---|
| Using service dates for one metric and documentation dates for another | A patient sits in one month's denominator and the next month's numerator. Contact rate and improvement both fall |
| Taking the date from a UTC timestamp | Evening events on the last day of the month land in the next month |
| Running the report on the 1st | Contacts and scales documented late are missed; contact rate is understated |
| Restating last month whenever late notes arrive | Submitted numbers never settle, and month-to-month trends can't be compared |

## For automation

- [`site_month.extract_run_date`](../../reference/data-contract.md#t8-site_month--one-row-per-submission):
  the calculator warns if it is earlier than the 15th of the following month.
- Every date column in the data contract is a local date, not a timestamp. Extraction
  converts to local time.
