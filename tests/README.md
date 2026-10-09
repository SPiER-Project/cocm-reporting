# Tests

The guide's worked examples, as data a calculator can be tested against, and the
bookkeeping that keeps them in step with the calls.

| Path | What it is |
|---|---|
| [`fixtures/example-caseload/`](fixtures/example-caseload/) | The ten patients of the [example caseload](../docs/guide/example-caseload.md), metrics 1–8 |
| [`fixtures/screening-example/`](fixtures/screening-example/) | The eight patients of the [screening example](../docs/guide/concepts/screening.md#worked-example), metrics 9–10 |
| [`examples.toml`](examples.toml) | Every worked example in the guide, the pages that show it, and the calls it depends on |
| `examples.lock.json` | The fingerprint of each call when each example was last verified. Written by `scripts/examples.py verify`; don't edit it |

## Fixtures

Each fixture directory holds one CSV per [data-contract](../docs/reference/data-contract.md)
table (header only where a table isn't used) and an `expected.toml` with the results.

CSV conventions:
- dates are `YYYY-MM-DD`;
- booleans are `true` or `false`;
- a blank cell is an empty value;
- `billing_codes` lists codes separated by `;`.

`expected.toml` states counts, not percentages. The percentages and weeks the pages show
are computed from the counts with the [rounding rule](../docs/reference/our-calls.md#rounding).
It also lists per-patient facts, so a failing calculator test can say which patient
differs and why.

## Checks

```bash
python3 scripts/examples.py check
```

It confirms three things:
- every fixture matches the data contract;
- every page shows the results that `expected.toml` implies;
- no example is stale.

An example is stale when a call it depends on has changed since it was last verified. A
call has changed when its values in `rules/calls.toml` change, or when the wording of its
"Call." paragraph in `our-calls.md` changes. Changing a call's status or approval doesn't
count.

## When there's a calculator

Its test suite should run it on each fixture and compare the output with
`expected.toml`, metrics first, then patients.
