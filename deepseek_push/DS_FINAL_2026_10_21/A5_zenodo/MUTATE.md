# MUTATE — proof that the quote check has teeth

## The mutation

`python3 a5_checks.py --mutate` replaces one number **inside a ledger quote**:

```
# MUTATE: 73.19 -> 73.91 in record 23251231 claim 0
```

`73.19` is the observed `Lambda c^4/a0^2` in the abstract of Zenodo 23251231
("with the RAR kernel the integral converges to 12.99, 5.6 times below the observed 73.19").
The record's own text is left untouched; only the ledger copy is corrupted, which is exactly the
drift the ledger must be unable to survive.

## Recorded output (captured verbatim, `_zenodo/mutate.out`)

```
# MUTATE: 73.19 -> 73.91 in record 23251231 claim 0
K1 PASS 178 records / 178 rows 178 / 178  # Zenodo reported total 178; 8 pages of <=25
K2 FAIL 624 verbatim / 625 quotes all verbatim  # first bad: [(23251231, 'The Lambda match needs the quadrature kernel with ')]
K3 FAIL 2954 numbers in-quote / 2955 all in-quote  # first miss: [(23251231, '73.19')]
K4 PASS 178 rows, 7 states 178 rows, states in taxonomy, counts match  # {"catalogued_only": 53, "integrated": 59, "not_applicable": 1, "only_zenodo": 6, "out_of_scope": 19, "paper_only": 21, "superseded": 19}
K5 PASS 178 matched / 178 all match  # first: []
K6 PASS 13 October records with 0/121 numbers in canon (20 numbers found overall) >=12 records  # canon = STANDING.md + FRAMEWORK_EQUATIONS_2026-10-15.md
K7 FAIL 13/14 clues complete all complete  # incomplete=[] quote_bad=['23251231']
K8 PASS 178 unique ids / 178 unique DOIs 178 / 178
K9 PASS 5/5 stored hashes; offline all match
K10 PASS mutation caught=True (K2 ok=False, K3 ok=False) mutation must break K2 or K3
A5_ZENODO MUTATE: 7/10 checks PASS (K10 PASS means the corruption was detected)
```

Exit code 0, which in `--mutate` mode means **the corruption was caught** (the mode returns 1 if a
mutation survives).

## What each failure proves

| check | without mutation | with mutation | what it proves |
|---|---|---|---|
| K2 verbatim | 625/625 | 624/625, names 23251231 | a quote that is not a substring of its abstract is caught, not tolerated |
| K3 numbers-in-quote | 2955/2955 | 2954/2955, names `73.19` | a number that does not occur in its own quote is caught |
| K7 clue integrity | 14/14 | 13/14, `quote_bad=['23251231']` | a corrupted load-bearing clue cannot silently remain in the report's set |

Three independent checks fail on a single-character change, so the ledger's central claim — "every
quoted number appears verbatim in its abstract" — is not decorative.

## Ordinary run keeps the same teeth

`a5_checks.py` (no flags) also runs K10, by corrupting an **in-memory copy** and requiring that the
same test rejects it:

```
K10 PASS corrupted copy rejected=True 73.19 -> 73.91 must fail K2/K3
A5_ZENODO COMPLETE: 10/10 checks PASS.
```

So the sensitivity is verified on every run, not only when `--mutate` is passed.
