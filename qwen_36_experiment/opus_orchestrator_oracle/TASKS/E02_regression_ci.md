# E02 — Wire the regression runner into the workflow
COST: S | script: `TOOLS/run_regression.py` already exists — use and extend it

> ENGINEERING / DATA task. Import `TOOLS/mi_constants.py` — never retype a constant.
> `../02_HOUSE_RULES.md` and `../03_NUMERIC_HAZARDS.md` apply.

## The task
`TOOLS/run_regression.py` re-runs every committed self-checking script and reports which fail. Make it part
of the routine so the corpus's "self-verifying" claim is continuously true rather than aspirational.

## Do
1. Run it over the whole `mi_*_2026.py` corpus (`--timeout 1800`). Expect it to take a while; use `--quick`
   for the fast subset day to day.
2. Record the baseline in `../LEDGER.md`: how many scripts, how many total checks, total runtime.
3. Any script that fails or times out: fix it or mark it in the ledger with the reason. A corpus with a
   silently failing script is worse than one with a documented failure.
4. Extend it: add a `--since <git-ref>` mode that only re-runs scripts touched since a ref, so it is cheap
   enough to run before every commit.

## Why this one matters
Two tautological checks and eight float64 hazards were caught here by hand. A runner catches regressions the
day they appear rather than the week someone re-reads the file.
