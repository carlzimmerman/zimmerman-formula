# A31 MUTATE — do the referee's checks have teeth?

`a31_checks.py --mutate` corrupts **the FINAL value** of check 01 (`Z = 5.7888100` becomes `5.78`)
before the comparison. The recomputation is unchanged; a suite that still passed would be vacuous.
It does not: check 01 reports MISMATCH and the process exits 1.

Baseline (`python3 a31_checks.py`): `29/35` match, six mismatches (`04, 23, 28, 29, 30, 33`),
`A31 COMPLETE ... 32 non-BACKED claims`, exit 0.

Mutated (`python3 a31_checks.py --mutate`): `28/35` match, seven mismatches
(`01, 04, 23, 28, 29, 30, 33`), exit 1.

```
$ python3 a31_checks.py --mutate
  01 MISMATCH Z = 2 sqrt(8 pi/3)                      FINAL=5.78   RECOMPUTED=5.788810036466141
        [MUTATION] the FINAL value for Z was corrupted to 5.78; this check must fail.
  ...
CLAIM LEDGER: 130 claims | BACKED 98 | OVERSTATED 17 | UNBACKED 1 | WRONG 14
NUMERIC CHECKS: 28/35 match FINAL_THEORY.md
MISMATCHES: 01, 04, 23, 28, 29, 30, 33
A31 COMPLETE: 35 numeric checks, 28 match, 7 mismatches; 32 non-BACKED claims.
EXIT=1
```

The captured run is `a31_MUTATE.out`; the baseline is `a31.out`.

## Why this is the right mutation

The lane's claim is not "the arithmetic is hard" — it is "the synthesis's numbers can be checked
against the constants". Corrupting a FINAL value is exactly the failure mode the lane exists to
catch: if the comparison were written to echo the lane's own results, or if the tolerance were
absurdly wide, the mutation would pass. It does not, so the comparison is live.

## Second, non-scripted mutation (documentation)

The ledger itself has a mutation control: changing a verdict from BACKED to OVERSTATED in
`a31_ledger.py` changes the counts printed in `a31.out` and stored in `a31_results.json`. The counts
are computed by `Counter` over the ledger, not typed; edit one row and the `CLAIM LEDGER` line moves.
That is why the counts in the report and the JSON agree by construction.